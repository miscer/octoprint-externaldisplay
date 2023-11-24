/*
 * View model for OctoPrint-ExternalDisplay
 *
 * Author: Michal Miskernik
 * License: AGPLv3
 */
$(function() {
    class ExternalDisplayViewModel {
        constructor() {
            this.imageUrl = ko.observable(getFrameImageHref());
            this.updateInterval = null;
        }

        updateImageUrl() {
            this.imageUrl(getFrameImageHref());
        }

        onTabChange(current, previous) {
            if (current === "#tab_plugin_externaldisplay") {
                this.updateInterval = setInterval(() => this.updateImageUrl(), 1000);
            } else if (this.updateInterval != null) {
                clearInterval(this.updateInterval);
                this.updateInterval = null;
            }
        }
    }

    function getFrameImageHref() {
        return EXTERNAL_DISPLAY.api.frame + "?t=" + new Date().getTime();
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: ExternalDisplayViewModel,
        elements: ["#tab_plugin_externaldisplay"],
        dependencies: [],
    });
});
