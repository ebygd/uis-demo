const workoutsC = {
    props: ["user"],
    emits: ["error", "success"],
    template: /*html*/`
    <div>
        <exercise-history
        v-bind:check_history="check_history"
        v-bind:user="user"
        v-on:closed-popup="resetIndex"
        ></exercise-history>
        
        <h1>Your Previous Workouts: </h1><br>
        <div v-if="workouts.length===0"><h3>No logged workouts yet!</h3></div>
        <label v-if="workouts.length>0">Display: 
            <select class="workoutsDisplayed inputs" v-model="workoutsDisplayed">
                <option v-for="n in workouts.length">{{ n }}</option>
            </select>
        </label>
        
        <div class="accent-container" v-for="(workout, index) in workouts.slice(0, workoutsDisplayed)">

            <i v-on:click="deleteWorkout(index)" class="fa fa-times remove-exercise"></i>
            
            <form class="table-style">
            <div id="new-workout-header">
                <label>Title: {{ workout[0][2] }}</label>
                <label class="date-right">Date: {{ workout[0][8] }}</label>
            </div>
                <table>
                    <tr class="thead">
                        <td>Exercise name</td>
                        <td>Sets</td>
                        <td>Reps</td>
                        <td>Weight</td>
                    </tr>
                    <tr v-for="element in workout"> <!-- element[3] is exercise_id for that exercise-->
                        <td v-on:click="checkHistory(element[3])" class="edit-exercise-input">{{ element[4] }}</td>
                        <td>{{ element[5] }}</td>
                        <td>{{ element[6] }}</td>
                        <td>{{ element[7] }} kg</td>
                    </tr>
                    
                </table>
                <br>
            </form>
        </div>
        
        <button class="btn load-more-btn" v-if="workoutsDisplayed < workouts.length" v-on:click="loadMore">Show more</button>
    </div>

    `,
    data: function() {
        return {
            date: "",
            workout_title: "",
            workout_date: "",
            workouts: [],
            workoutsDisplayed: localStorage.getItem("displayedWorkouts"),
            username: this.user,
            showPopup: false,
            check_history: null,
        }
    },
    created: async function() {     
        let response = await fetch("/resource/"+this.username+"/workouts");
        if (response.status == 200) {
            let result = await response.json();
            if (result) {
                // indexing for this.workouts:
                // this.workouts[which workout][which exercise in that workout][id/user/title/set/rep etc]
                this.workouts = result;
            }
        }
    },
    watch: {
        workoutsDisplayed: function () {
            localStorage.setItem('displayedWorkouts', this.workoutsDisplayed)
        }
      },
    methods: {
        checkHistory(index) {
            this.check_history = index;
        },
        resetIndex() {
            // When popup is closed, set index to null (to fix a bug where you couldn't check exercise history of same exercise twice in a row)
            this.check_history = null;
        },
        deleteWorkout: async function(index) {
            if (!confirm("Are you sure you want to delete this workout?")) {
                return
            }
            // [index] is which workout, [0] indicates first exercise in that workout, and next index is id/title/date etc
            let response = await fetch("/resource/workouts/"+this.workouts[index][0][0], {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                }
            });
            if (response.status == 200) {
                let result = await response.text()
                if (result) {                    
                    this.$emit('success', "Workout deleted");
                    
                    // delete from current workout list
                    this.workouts.splice(index, 1);
                    return
                } 
                this.$emit('error', "Could not delete workout");
        
            }
        },
        loadMore() {
            // after using dropdown menu, the index is turned into a string, so need to parseInt the string.
            this.workoutsDisplayed = parseInt(this.workoutsDisplayed) + 2;
            // stop workoutsDisplayed from going over workouts length:
            if (this.workoutsDisplayed > this.workouts.length ) {
                this.workoutsDisplayed = this.workouts.length;
            }
        },       
        
    }
}