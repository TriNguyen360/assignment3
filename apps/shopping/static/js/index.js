"use strict";

let app = {};

// Vue app data and methods
app.data = function() {
    return {
        items: [],          // Array to store shopping list items
        newItem: "",        // Text input for a new item
    };
};

app.methods = {
    // Load initial data from the server and sort it
    load_data: async function () {
        try {
            let response = await axios.get(load_data_url);
            this.items = response.data.items;
            this.sortItems(); // Sort items after loading to ensure order
        } catch (error) {
            console.error("Error loading data:", error);
        }
    },

    // Add a new item, then reload and sort data
    addItem: async function () {
        if (!this.newItem.trim()) return; // Prevent empty items

        try {
            let response = await axios.post(add_item_url, { item_name: this.newItem });
            if (response.data.message) {
                this.newItem = ""; // Clear the input field
                this.load_data(); // Reload data to refresh order
            }
        } catch (error) {
            console.error("Error adding item:", error);
        }
    },

    // Toggle purchase status of an item, then reload and sort data
    togglePurchased: async function (item) {
        try {
            await axios.post(mark_purchased_url, {
                item_id: item.id,
                is_purchased: item.is_purchased,
            });
            this.load_data(); // Reload data to apply the new checked/unchecked order
        } catch (error) {
            console.error("Error toggling purchase status:", error);
        }
    },

    // Delete an item and reload data to refresh the order
    deleteItem: async function (item_id) {
        try {
            await axios.post(delete_item_url, { item_id: item_id });
            this.load_data(); // Reload data after deletion
        } catch (error) {
            console.error("Error deleting item:", error);
        }
    },

    // Sort items to ensure unchecked items stay at the top, checked items move to the bottom
    sortItems: function () {
        this.items.sort((a, b) => {
            if (a.is_purchased === b.is_purchased) {
                if (!a.is_purchased) {
                    // Both items are unchecked, sort by added_on descending (newer items first)
                    return new Date(b.added_on) - new Date(a.added_on);
                } else {
                    // Both items are checked, sort by checked_on ascending (earlier checked items first)
                    return new Date(a.checked_on) - new Date(b.checked_on);
                }
            }
            // Unchecked items (false) should be sorted above checked items (true)
            return a.is_purchased - b.is_purchased;
        });
    },
},    

// Initialize Vue app
app.vue = Vue.createApp({
    data: app.data,
    methods: app.methods,
    created() {
        this.load_data();  // Load data when the app is created
    },
}).mount("#app");