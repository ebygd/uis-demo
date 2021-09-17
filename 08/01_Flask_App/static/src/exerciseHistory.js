const exerciseHistoryC = {
    props: ["check_history", "user"],
    emits: ["closed-popup"],
    template: /*html*/`
    <div class="dim-background" v-if="showPopup" v-on:click="closeHistory"></div>
        <div class="popup" v-if="showPopup">
                    <i class="close-popup-icon fa fa-times" v-on:click="closeHistory"></i>
                    <form class="table-style">
                        <table>
                            <tr v-if="exercise_history.length !== 0">
                                <th>Exercise</th>
                                <th>Set x Reps</th>
                                <th>Weight</th>
                                <th>Date</th>

                            </tr>
                            <tr v-for="exercise in exercise_history" v-if="exercise_history.length !== 0">
                                <td>{{ exercise.exercise }}</td>
                                <td>{{ exercise.sets }} x {{ exercise.reps }}</td>
                                <td>{{ exercise.weight }} kg</td>
                                <td>{{ exercise.date }}</td>
                            </tr>
                            <tr v-else>No records for this exercise</tr>
                        </table>
                    </form>
                </div>
    `,
    data() {
        return {
            showPopup: false,
            exercise_history: [],
        }
    },
    watch: {
        check_history() {
            // when the var is changed in parent component, we check history for that exercise (but not when it is being reset back to null)
            if (this.check_history !== null) {
                this.exerciseHistory(this.check_history);
            }
        }
    },
    methods: {
        exerciseHistory: async function (index) {
            this.showPopup = true;
            let response = await fetch("/resource/"+this.user+"/workouts/exercise/"+index);
            if (response.status === 200) {
                let result = await response.json();
                this.exercise_history = result;
                return
            }
        },
        closeHistory() {
            this.showPopup = false;
            this.$emit("closed-popup");
        }
    }
}