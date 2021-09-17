const loginC = {
    emits: ["new-login", "success", "info"],
    template: /*html*/`
    <div>
        <div class="login-error">{{ err }}</div>
        <div class="login-register-container">
            <form action="javascript:void(0);"><br>
                <h2>Login</h2><br>
                <table>
                    <tr><input class="inputs login-input" type="text" placeholder="Username" v-model="username"></tr>
                    <tr><input class="inputs login-input" type="password" placeholder="Password" v-model="password"></tr>
                    <tr><input class="inputs login-input invis"></tr><br>
                    <tr><input class="login-register-btn" type="submit" value="Log in" v-on:click="login" ></tr>
                </table>
            </form>

            <form action="javascript:void(0);"><br>
                <h2>Register</h2><br>
                <table>
                    <tr><input class="inputs login-input" type="text" placeholder="Username" v-model="reg_username"></tr>
                    <tr><input class="inputs login-input" type="text" placeholder="Email" v-model="reg_email"></tr>
                    <tr><input class="inputs login-input" type="password" placeholder="Password" v-model="reg_password"></tr><br>
                    <tr><input class="login-register-btn" type="submit" value="Register" v-on:click="register"></tr>
                </table>
            </form>
        </div>
    </div>
    `,
    data() {
        return {
            username: "",
            email: "",
            password: "",

            reg_username: "",
            reg_email: "",
            reg_password: "",
            err: ""
        }
    },
    methods: {
        login: async function() {
            // Check for empty fields:
            if (this.username === "" || this.password === "") {
                this.displayError("No Empty Fields");
                return
            }

            let response = await fetch("/resource/session", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: this.username, password: this.password }),
            });
            if (response.status == 200) {
                let result = await response.json();
                if (result) {
                    this.show_login_form = !this.show_login_form;
                    this.user = result["username"];
                    
                    // let app.js know there is a new login
                    this.$emit("new-login", result);
                    this.$emit("info", this.user + " logged in");
                    
                    // redirect to all workouts
                    this.$router.push("/");
                    return
                } 
                // If there is an error:
                this.displayError("Invalid login info");
                
            }
            
        },
        register: async function() {
            if (this.reg_username === "" || this.reg_password === "" || this.reg_email === "") {
                this.displayError("No Empty Fields");
                return
            }
            let response = await fetch("/user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: this.reg_username, email: this.reg_email, password: this.reg_password }),
            });
            if (response.status == 200) {
                let result = await response.json();
                if (result === "username taken") {
                    this.displayError("Username is already in use");
                    return
                }
                if (result === "email taken") {
                    this.displayError("Email is already in use");
                    return
                }
                // if success:
                if (result) {
                    this.user = result["username"];

                    // let app.js know there is a new login
                    this.$emit("new-login", result);
                    this.$emit("info", "Welcome " + this.reg_username);

                    // redirect new user to new-workout page
                    this.$router.push("/new-workout");
                    return
                }
                this.displayError("Username should be above 3 characters");
                
            }
        },
        displayError(msg) {
            this.err = msg;
            // if its a longer msg, give it more time to be displayed
            if (msg.length > 30) {
                setTimeout(() => {
                    this.err = "";
                }, 4000);
                return
            }
            setTimeout(() => {
                this.err = "";
            }, 2000);
        }
    }

}