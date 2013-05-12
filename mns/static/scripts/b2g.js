var b2g = null;
function check_b2g(){

    if (typeof MozActivity != "function") {
        return;
    }
    b2g = {
        manifest_url: "http://localhost:8000/static/manifest.webapp",

        install: function(event)
        {
            event.preventDefault();
            var myapp = navigator.mozApps.install(b2g.manifest_url);
            myapp.onsuccess = function(data) {
                // App is installed, remove install button
                $(".install.b2g").remove();
            };
            myapp.onerror = function() {
                console.log(this.error.name);
            };
        },

        pick_img: function()
        {
            var pickImg = new MozActivity({
                    name: "pick",
                    data: {
                        type: ["image/jpg", "image/jpeg", "img/png"]
                    }
            });
            pickImg.onsuccess = function () {
                var blob = this.result.blob;
                $("#profile_image").prop("src",
                        window.URL.createObjectURL(blob));
            };
        }
    };

    $(document).on("click", "button.install.b2g", b2g.install);
    $(document).on("click", "#profile_image", b2g.pick_img);
    $(".b2g").addClass("show");
}
check_b2g();
