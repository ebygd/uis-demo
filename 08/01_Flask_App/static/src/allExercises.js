const allExercisesC = {
    props: ["user", "userid", "new_exercise_id"],
    emits: ["new-exercise", "success", "error", "save"],
    template: /*html*/ `
    <div>
        <h1>All Available Exercises: </h1>

        <create-exercise 
        v-on:new-exercise="newExercise($event)" 
        v-on:error="$emit('error', $event)">
        </create-exercise>

        <exercise-list
        v-bind:user="user"
        v-bind:userid="userid"
        v-bind:new_exercise_id="new_exercise_id"
        v-bind:new_exercise="new_exercise"
        v-on:success="$emit('success', $event)"
        v-on:error="$emit('error', $event)"
        >
        </exercise-list>
        
    </div>

    `,
    data: function() {
        return {
            new_exercise: { exercise_name: "", category: "", body_part: "" },
        }
    },
    methods: {
        newExercise(exercise) {
            // this.new_exercise is sent as prop to exerciseListC
            this.new_exercise = exercise;
            // emit the new exercise to app.js, as well as a flag indicating a non-global exercise:
            // the emitted exercise will be in format:
            // { exercise: Proxy, global_exercise: 0/1 } (see createExercise(event) in app.js)
            this.$emit("new-exercise", {exercise: this.new_exercise, global_exercise: 0});
        }
    }
}