
var shopEditorItems = new Tour({
    steps: [
        {
            element: "#menuContainer",
            title: "How To: Edit Shop",
            content: "Welcome to Tinville and our quick tour of how to create a shop."
        },
        {
            element: "#addItemImg",
            title: "How To: Edit Shop",
            content: "To Add a new Item click the Add Item Icon.",
            onNext: function(tour) {
                showModal();
            }
        },
        {
            element: "#hiddenShopperField",
            template: "",
            duration: 1000
        },
        {
            element: "#id_title",
            title: "How To: Edit Shop",
            content: "Enter the name of the product."
        },
        {
            element: "#id_description_ifr",
            title: "How To: Edit Shop",
            content: "Enter the description of the product."
        },
        {
            element: "#id_category",
            title: "How To: Edit Shop",
            content: "Select the category of the product."
        },
        {
            element: "#id_price",
            title: "How To: Edit Shop",
            content: "Set the price of the product."
        },
        {
            element: "#id_images-0-original",
            title: "How To: Edit Shop",
            content: "Upload an image of the product."
        },
        {
            element: "#div_id_sizeVariation",
            title: "How To: Edit Shop",
            content: "Select the size of the product."
        },
        {
            element: "#itemModalFooterSubmit",
            title: "How To: Edit Shop",
            content: "Submit the new product or click close to cancel."
        }
    ]});

shopEditorItems.init();

$("#editorTour").click(function() {
    shopEditorItems.restart();
});