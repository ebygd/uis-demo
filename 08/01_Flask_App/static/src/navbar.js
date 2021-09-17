const navbarC = {
    props: ["theme", "username"],
    emits: ["user-loggedout", "info", "mode-toggle"],
    template: /*html*/` 
    <div> 
        <i id="logo-text">Workout Logger</i>
        
        <input type="button" class="show-btn" id="show-right-btn" value="Log out" v-on:click="logout" v-if="username!==''"><br><br><br>
        <i class="loggedin-text" v-if="username!==''">Logged in as: {{ this.username }}</i>
    
        <div id="img"></div>

        <div class="mode-container">
            <p class="toggle-text">Dark Mode:</p>
            <label class="switch">
                <input type="checkbox" v-on:click="$emit('mode-toggle')" v-bind:checked="this.theme=='dark'">
                <span class="slider round"></span>
            </label>
        </div>

    </div>
    `,
    methods: {
        logout: async function() {
            let response = await fetch("/resource/session", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                }
            });
            if (response.status == 200) {
                let result = await response.json();
                if (result) {
                    this.$emit("user-loggedout");
                    this.$emit("info", "Good Bye!");
                }
            }
        }

    }
}