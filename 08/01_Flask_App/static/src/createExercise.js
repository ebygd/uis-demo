const createExerciseC = {
    emits: ["new-exercise", "error"],
    template: /*html*/ `
    <div id="new-workout-container">
        <div class="new-exercise-container accent-container">
            <p>Create a custom exercise: </p>
            <form>
                <input type="text" id="exercise-name-input" size="20" placeholder="Exercise name" v-model="exercise_name">
                <select name="category" id="exercise-category-input" v-model="category">
                <option value="" disabled selected hidden>Category</option>
                    <option v-for="option in categories" v-bind:value="option">
                    {{ option }}
                    </option>
                </select>
                <select name="body_part" id="exercise-bodypart-input" v-model="body_part">
                <option value="" disabled selected hidden>Body Part</option>
                    <option v-for="option in body_parts" v-bind:value="option">
                    {{ option }}
                    </option>
                </select>
                <input type="button" class="btn new-ex-btn" value="Add Exercise" v-on:click="createExercise">
            </form>
        </div>
    </div>
    `,
    data: function() {
        return {
            exercise_name: "",
            category: "",
            body_part: "",
            categories: ["Dumbbell", "Barbell", "Machine", "Cable", "Bodyweight", "Other"],
            body_parts: ["Chest", "Shoulder", "Back", "Legs", "Arms", "Core", "Full Body", "Olympic", "Cardio", "Other"],

        }
    },
    methods: {
        createExercise: function() {
            // emit event: send exercise-dict to app.js (if fields are not empty)
            if (this.exercise_name === "" || this.category === "" || this.body_part === "") {
                this.$emit('error', "Please fill in all fields");
                return
            }
            // Emit to parent component that a new exercise has been added.
            this.$emit('new-exercise', { exercise_name: this.exercise_name, category: this.category, body_part: this.body_part});
            this.exercise_name = "";
            this.category = "";
            this.body_part = "";
        },
    }
}