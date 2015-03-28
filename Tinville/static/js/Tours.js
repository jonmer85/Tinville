function aboutPageFunc() {
        $("#aboutTabAnchor").click();
}
function aboutProfileFunc() {
        $('#aboutBoxModal').modal();
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
            content: "Here you can enter your Shop Profile information. Click Submit to save your changes or click cancel.",
            onNext: shopProfileFunc
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