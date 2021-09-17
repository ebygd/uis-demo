let app = Vue.createApp({
        data: function(){
        return {
            mode: "light",
            success: "",
            info: "",
            error: "",
            user: "",
            userid: "",
            role: "",
            email: "",
            new_exercise_id: null,
            
        }
    },
    created: async function() {
        // set initial value of workouts displayed (for workouts component)
        if (localStorage.getItem("displayedWorkouts") === null) {
            localStorage.setItem('displayedWorkouts', 3);
        }
        let response = await fetch("/resource/session", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        if (response.status == 200) {
            let result = await response.json();
            if (result !== false) {
                this.user = result["username"];
                this.userid = result["id"];
                this.role = result["role"];
                this.email = result["email"];
            }
        }
        let userMode = localStorage.getItem("mode");
        if (userMode == "dark") {
            this.mode = "dark";
        }
        document.documentElement.setAttribute("theme", userMode);
        
    },
    
    methods: {
        newLogin(user) {
            this.user = user["username"];
            this.role = user["role"];
            this.email = user["email"];
            this.userid = user["id"];
        },
        newLogout() {
            this.user = "";
            this.role = "";
            this.email = "";
            this.userid = "";
            
        },
        toggleModes() {
            if (this.mode == "dark") {
                this.mode="light";
            } else {
                this.mode="dark";
            }
            document.documentElement.setAttribute("theme", this.mode);
            localStorage.setItem("mode", this.mode);
        },
        createExercise: async function(exercise) {
            // exercise is object: { exercise: Proxy, global_exercise: 0/1 }, so need to access exercise.exercise["___"] to access exercise itself
            // checking for empty fields is done before emitting to app.js, so we save ourselves an unneccessary get request
            let response = await fetch("/resource/"+this.user+"/exercises", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ exercise_name: exercise.exercise["exercise_name"], category: exercise.exercise["category"], body_part: exercise.exercise["body_part"], global: exercise.global_exercise }),
            });
            if (response.status == 200) {
                this.successAlert("Exercise '"+exercise.exercise["exercise_name"]+ "' created");

                // Backend returns the new exercise ID, sending this ID back to the component exerciseList, 
                // so I can add the new exercise to the list of workouts with correct ID,
                // without having to send new GET request to update the list
                this.new_exercise_id = await response.json();
            }

        },
        // different types of alerts are displayed for 2sec
        successAlert: function(message) {
            this.success = message;
            setTimeout(() => {
                this.success = "";
            }, 2000);
        },
        errorAlert: function(message) {
            this.error = message;
            setTimeout(() => {
                this.error = "";
            }, 2000);
        },
        infoAlert: function(message) {
            this.info = message;
            setTimeout(() => {
                this.info = "";
            }, 2000);
        },        
    },
});
app.use(router);
app.component("navbar-c", navbarC)
app.component("admin-page", adminPageC);
app.component("workout-form", newWorkoutFormC);
app.component("workouts", workoutsC);
app.component("all-exercises", allExercisesC);
app.component("mypage", mypageC);
app.component("create-exercise", createExerciseC);
app.component("log-in", loginC);
app.component("exercise-list", exerciseListC);
app.component("exercise-history", exerciseHistoryC);
app.mount("#app");