const newWorkoutFormC = {
    props: ["user"],
    emits: ["new-exercise", "success", "error"],
    template: /*html*/`
    <div>
        <h1>Log a New Workout: </h1>
        
        <div id="">
            <div class="accent-container">
                <form class="table-style">
                    <div id="new-workout-header">
                        <label>Workout Title: <input type="text" v-model="this.title" placeholder="unnamed workout"></label>
                        <label>Enter the Date: <input type="date" v-model="this.date"></label>
                    </div>
                    <table>
                        <tr class="thead">
                            <td>Exercise name</td>
                            <td>Sets</td>
                            <td>Reps</td>
                            <td>Weight</td>
                            <td v-if="rowCount>1"></td>
                        </tr>
                        <tr v-for="(exercise, index) in workout">
                            <td>
                            <select name="exercise_name" class="exercise_select" v-model="exercise.exercise_name">
                                <option value="" disabled selected hidden>exercise</option>
                                <option v-for="user_exercise in user_exercises" v-bind:value="user_exercise.exercise_name">{{ user_exercise.exercise_name }}</option>
                            </select></td>
                            <td><input class="inputs" type="number" min="0" placeholder="sets" v-model="exercise.sets"></td>
                            <td><input class="inputs" type="number" min="0" placeholder="reps" v-model="exercise.reps"></td>
                            <td><input class="inputs" type="number" min="0" placeholder="weight" v-model="exercise.weight"></td>
                            <td><i v-if="rowCount>1" v-on:click="removeRow(index)" class="fa fa-times"></i></td>
                        </tr>
                        <tr>
                            <td><input type="button" class="btn" value="Add a row" v-on:click="addRow"></td>
                            <td></td>
                            <td></td>
                            <td><input type="button" class="btn" value="Save" v-on:click="checkFields"></td>
                            <td v-if="rowCount>1"></td>
                        </tr>
                    </table>
                </form>
            </div>
        </div>
    </div>
    `,
    data: function() {
        return {
            categories: ["Dumbbell", "Barbell", "Machine", "Cable", "Bodyweight", "Other"],
            body_part: ["Chest", "Shoulder", "Back", "Legs", "Arms", "Core", "Full Body", "Olympic", "Cardio", "Other"],
            title: "",
            date: "",
            workout: [{ title: "", exercise_name: "", sets: "", reps: "", weight: "", date: ""}],
            user_exercises: [],
            username: this.user,
            rowCount: 1
        }
    },
    created: async function() {
        //  on load: load all exercises into this.user_exercises so I can sort on it
        let response = await fetch("/resource/"+this.username+"/exercises", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.status == 200) {
            let result = await response.json();
            if (result) {
                this.user_exercises = result;
            }
        }
    },

    methods: {
        addRow: function() {
            this.workout.push({title: "", exercise_name: "", sets: "", reps: "", weight: "", date: "" });
            this.rowCount++;

        },
        removeRow: function(index) {
            this.workout.splice(index, 1);
            this.rowCount--;            

        },
        checkFields() {
            if (this.date === "") {
                this.$emit('error', "Please enter a workout date");
                return 
            }
            if (this.title === "") {
                this.title = "Unnamed Workout";
            }
            let emptyField = false;
            this.workout.forEach(exercise => {
                // If there isn't an exercise for each row added: alert error and return
                if (exercise["exercise_name"] === "") {
                    this.$emit("error", "An exercise is missing");
                    emptyField = true;
                    return
                } else {
                    // append date and title to each exercise in that workout
                    exercise["title"] = this.title;
                    exercise["date"] = this.date;
                }
            });
            // return from not only the forEach, but the method itself:
            if (emptyField) {
                return
            }
            // After checking fields and assigning title + date to all exercises we save the workout to db.
            this.saveWorkout();
        },
        saveWorkout: async function() {
            // send the workout to flask:
            let response = await fetch("/resource/"+this.username+"/workouts", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(this.workout)
            });
            if (response.status == 200) {
                let result = await response.json()
                // Flask returns true if success:
                if (result) {
                    // Emit success msg
                    this.$emit('success', this.title + " was saved")
                    // then reset input fields
                    this.workout = [{ title: "", exercise_name: "", sets: "", reps: "", weight: "", date: ""}];

                    this.title = "";
                    this.date = "";
                    return
                } 
                // emit an error if something went wrong.
                this.$emit('error', "Something went wrong");
                
            }
            
        },

    }
}