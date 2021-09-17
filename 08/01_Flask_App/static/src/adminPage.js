const adminPageC = {
    props: ["user", "userid", "new_exercise_id"],
    emits: ["new-exercise", "error", "success"],
    template: /*html*/`
    <div>
        <h2>Create a Global Exercise: </h2>
        <div id="new-workout-container">
            <div class="accent-container">
                
                <create-exercise
                v-on:new-exercise="newExercise($event)"
                v-on:error="$emit('error', $event)">
                </create-exercise>
                
            </div>
        </div>
        <h2>Remove or Edit a Global Exercise: </h2>
        
        <exercise-list
        v-bind:admin="admin"
        v-bind:user="user"
        v-bind:userid="userid"
        v-bind:new_exercise_id="new_exercise_id"
        v-bind:new_exercise="new_exercise"
        v-on:success="$emit('success', $event)"
        v-on:error="$emit('error', $event)"
        ></exercise-list>
        
    </div>
    `,

    data: function() {
        return {
            admin: true,
            new_exercise: { exercise_name: "", category: "", body_part: "" },
        }
    },
    methods: {
        newExercise(exercise) {
            this.new_exercise = exercise;
            // emit exercise to app.js with flag 1 indicating global exercise
            this.$emit("new-exercise", {exercise: this.new_exercise, global_exercise: 1});
        }
    }
        

}
