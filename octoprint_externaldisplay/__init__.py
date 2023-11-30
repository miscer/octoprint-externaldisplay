# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from octoprint_externaldisplay import canvas
from octoprint_externaldisplay.framebuffer import Framebuffer
from octoprint_externaldisplay.loop import RenderLoop
from octoprint_externaldisplay.views import print
import flask
import io


class ExternaldisplayPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.BlueprintPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.ShutdownPlugin,
):
    canvas = None
    view = None
    framebuffer = None

    def get_view_data(self):
        temperatures = self._printer.get_current_temperatures()
        current_data = self._printer.get_current_data()

        bed_temp, extruder_temp = None, None

        if "bed" in temperatures:
            bed_temp = print.Temperature(
                current=temperatures["bed"]["actual"],
                target=temperatures["bed"]["target"]
            )
        if "tool0" in temperatures:
            extruder_temp = print.Temperature(
                current=temperatures["tool0"]["actual"],
                target=temperatures["tool0"]["target"]
            )

        return print.PrintViewData(
            bed=bed_temp,
            extruder=extruder_temp,
            progress=current_data["progress"]["completion"],
            time_elapsed=current_data["progress"]["printTime"],
            time_remaining=current_data["progress"]["printTimeLeft"],
        )

    def draw_frame(self):
        data = self.get_view_data()
        self.view.draw(data)

    ##~~ StartupPlugin mixin

    def on_after_startup(self):
        self.create_framebuffer()
        self.create_canvas()

        self.view = print.PrintView(self.canvas)

        self.render_loop = RenderLoop(self)
        self.render_loop.start()

    def create_framebuffer(self):
        active = self._settings.get_boolean(["enable_framebuffer"])
        path = self._settings.get(["framebuffer_path"])

        if active and path:
            self.framebuffer = Framebuffer(path)
            self._logger.info(f"Framebuffer size: {self.framebuffer.get_size()}")
            self._logger.info(f"Framebuffer color depth: {self.framebuffer.get_color_depth()}")
        else:
            self._logger.info("Framebuffer not active")

    def create_canvas(self):
        size = (128, 128)

        if self.framebuffer:
            size = self.framebuffer.get_size()

        self.canvas = canvas.Canvas(size)

    ##~~ ShutdownPlugin mixin

    def on_shutdown(self):
        self.render_loop.stop()

        if self.framebuffer:
            self.framebuffer.close()

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "enable_framebuffer": False,
            "framebuffer_path": "",
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/externaldisplay.js"],
            "css": ["css/externaldisplay.css"],
            "less": ["less/externaldisplay.less"]
        }

    ##~~ BlueprintPlugin mixin

    def is_blueprint_csrf_protected(self):
        return True

    def is_blueprint_protected(self):
        return False

    @octoprint.plugin.BlueprintPlugin.route("/frame", methods=["GET"])
    def api_frame(self):
        if not self.canvas:
            return flask.abort(503)

        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        self.canvas.get_image().save(image_io, format='PNG')
        image_io.seek(0)

        # Return the image in the response
        return flask.send_file(image_io, mimetype='image/png')

    @octoprint.plugin.BlueprintPlugin.route("/info", methods=["GET"])
    def api_info(self):
        return flask.jsonify(self.get_view_data()._asdict())

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "externaldisplay": {
                "displayName": "External Display",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "miscer",
                "repo": "octoprint-externaldisplay",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/miscer/octoprint-externaldisplay/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "External Display"

# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ExternaldisplayPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
