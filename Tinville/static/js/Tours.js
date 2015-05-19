function aboutPageFunc() {
        $("#aboutTabAnchor").click();
}
function aboutProfileFunc() {
        $('#aboutBoxModal').modal();
}
function shopBannerFunc() {
    $("#bannerUploadModal").modal();
}
function shopBannerClose() {
    $("#bannerUploadModal").modal('hide');
}
function shopColorFunc() {
    $("#colorPickerModal").modal();
}
function shopColorClose() {
    $("#colorPickerModal").modal('hide');
}
function shopProfileFunc() {
    $("#aboutBoxModal").modal('hide');
}
function backToShopTab() {
    $("#shopTabAnchor").click();
}
function addItemIconFunc() {
    $('#productCreationModal').modal();
}
function endItemFunc() {
    $("#productCreationModal").modal('hide');
}
var shopEditorItems;
shopEditorItems = new Tour({
    steps: [
        {
            element: "#editorTour",
            title: "How To: Edit Shop",
            content: "Welcome to Tinville and our quick tour of how to create a shop."
        },
        {
            element: ".bannerUploadEditButton",
            title: "How To: Edit Shop",
            content: "This button enables you to change your banner image.",
            onNext: shopBannerFunc
        },
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
        {
            element: "#bannerModalFooterSubmit",
            title: "How To: Edit Shop",
            content: "Select your desktop and mobile banner images and click submit to upload.",
            onNext: shopBannerClose
        },
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
        {
            element: "#aboutTabAnchor",
            title: "How To: Edit Shop",
            content: "This tab brings you to the 'About' your shop page.",
            onNext: aboutPageFunc
        },
        {
            element: "#aboutAddProfileBtn",
            title: "How To: Edit Shop",
            content: "Click the 'Add Your Profile' button to access your shop profile information.",
            onNext: aboutProfileFunc
        },
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
        {
            element: "#div_id_aboutImg",
            title: "How To: Edit Shop",
            content: "Here you can enter your Shop Profile information. Click Submit to save your changes or click close.",
            onNext: shopProfileFunc
        },
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
{
    element: ".colorPickerEditButton",
        title: "How To: Edit Shop",
    content: "To change your banner color click the Banner Color edit button.",
    onNext: shopColorFunc
},
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
        {
            element: "#colorModalFooterSubmit",
            title: "How To: Edit Shop",
            content: "Select your new banner color and click submit to save or close to cancel.",
            onNext: shopColorClose
        },

        {
            element: "#shopTabAnchor",
            title: "How To: Edit Shop",
            content: "To go back to your shop click the Shop Tab.",
            onNext: backToShopTab
        },
        {
            element: "#addItemImg",
            title: "How To: Edit Shop",
            content: "To Add a new Item click the Add Item Icon.",
            onNext: addItemIconFunc
        },
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
        {
            element: "#id_title",
            title: "How To: Edit Shop",
            content: "Please enter all the product fields. Don't forget to scroll!"
        },
        {
            element: "#productCreateModelClose",
            title: "How To: Edit Shop",
            content: "Submit the new product or click close to cancel.",
            onNext: endItemFunc
        }
    ]
});

$("#editorTour").click(function() {
    shopEditorItems.init();
    shopEditorItems.restart();
});