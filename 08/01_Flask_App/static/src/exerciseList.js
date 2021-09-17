const exerciseListC = {
    props: ["user", "userid", "new_exercise_id", "new_exercise", "admin"],
    emits: ["new-exercise", "success", "error"],
    template: /* html*/`
    <div>
        <exercise-history
        v-bind:check_history="check_history"
        v-bind:user="user"
        v-on:closed-popup="resetIndex"
        ></exercise-history>
            <div class="accent-container">
                <div class="search-entry">
                    <label for="search">Search: <input type="text" placeholder="exercise name" v-model="keyword"></label>
                    <div class="filters">
                        <select v-model="search_category">
                            <option value="">Any category</option>
                            <option v-for="category in categories">{{ category }}</option>
                        </select>
                        <select v-model="search_bodypart">
                            <option value="">Any body part</option>
                            <option v-for="part in body_part">{{ part }}</option>
                        </select>
                    </div>
                </div>

                <div class="edit-exercise-label">
                    <p v-if="!admin">You can edit a non-global exercise by clicking the edit icon</p>
                    <p v-if="admin">You can edit a global exercise by clicking the edit icon</p>
                    <p>
                        Click on a table header to sort on it
                        <br>
                        Click on an exercise to see every time that exercise has been logged
                    </p>
                </div>

            <div>
                <div>
                    <table id="all-exercises-table">
                        <thead>
                            <tr>                                                                    <!-- sorting icon class is assigned to current sortdirection and "sort-group" -->
                                <th @click="sort('exercise_name')">Exercise Name <i v-bind:class="{ 'fa fa-sort-desc': currentSortDir=='desc' && currentSort=='exercise_name', 'fa fa-sort-asc': currentSortDir=='asc' && currentSort=='exercise_name' }"></i></th>
                                <th @click="sort('category')">Category <i v-bind:class="{ 'fa fa-sort-desc': currentSortDir=='desc' && currentSort=='category', 'fa fa-sort-asc': currentSortDir=='asc' && currentSort=='category' }"></i></th>
                                <th @click="sort('body_part')">Body Part <i v-bind:class="{ 'fa fa-sort-desc': currentSortDir=='desc' && currentSort=='body_part', 'fa fa-sort-asc': currentSortDir=='asc' && currentSort=='body_part' }"></i></th>
                                <th @click="sort('global_exercise')">Global <i v-bind:class="{ 'fa fa-sort-desc': currentSortDir=='desc' && currentSort=='global_exercise', 'fa fa-sort-asc': currentSortDir=='asc' && currentSort=='global_exercise' }"></i></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(exercise, index) in filteredExercises">

                                <td v-if="indexToEdit === index && indexToEdit !== '' ">
                                    <input class="edit-exercise-input" :placeholder="exercise['exercise_name']"
                                        v-model="editedName">

                                </td>
                                <td v-else class="edit-exercise-input" v-on:click="checkHistory(index)">
                                {{ exercise["exercise_name"] }}</td>

                                <td v-if="indexToEdit === index">
                                    <select name="category" id="exercise-category-input" v-model="editedCategory">
                                        <option v-for="option in categories" v-bind:value="option">
                                            {{ option }}
                                        </option>
                                    </select>
                                </td>
                                <td v-else>{{ exercise["category"] }}</td>

                                <td v-if="indexToEdit === index">
                                    <select name="body_part" id="exercise-bodypart-input" v-model="editedBodyPart">
                                        <option v-for="option in body_part" v-bind:value="option">
                                            {{ option }}
                                        </option>

                                    </select>

                                </td>
                                <td v-else>{{ exercise["body_part"] }}</td>

                                <td v-if="indexToEdit === index">
                                    <input type="submit" class="btn" value="save" v-on:click="saveEdit(index)"><br><br>
                                    <input type="submit" class="btn" value="cancel" v-on:click="cancelEdit(index)">
                                </td>

                                <td v-else>
                                <!-- if exercise is not global: display edit and delete options, or if user is admin we also display them-->
                                    <i v-if="this.admin || exercise['global_exercise'] == 0" v-on:click="changeIndexToEdit(index)"
                                        class="fa fa-pencil-square-o"></i>
                                    <i v-if="this.admin || exercise['global_exercise'] == 0" v-on:click="deleteExercise(index)"
                                        class="fa fa-times"></i>

                                    <i v-else class="">global</i>
                                </td>

                            </tr>
                        </tbody>
                    </table><br>
                </div>
                
            </div>
        </div>
    </div>
    `,
    data: function () {
        return {
            exercises: [],
            categories: ["Dumbbell", "Barbell", "Machine", "Cable", "Bodyweight", "Other"],
            body_part: ["Chest", "Shoulder", "Back", "Legs", "Arms", "Core", "Full Body", "Olympic", "Cardio", "Other"],

            search_bodypart: "",
            search_category: "",
            keyword: "",

            indexToEdit: "",
            editedName: "",
            editedCategory: "",
            editedBodyPart: "",

            currentSortDir: "asc",
            currentSort: "name",
            check_history: null,
        }
    },
    watch: {
        new_exercise() {
            // watch this.new_exercise to create it upon arrival
            this.createExercise(this.new_exercise);
        }
    },
    created: async function () {
        // if we are accessing the exerciselist from 
        if (this.admin) {
            this.loadGlobalExercises();
            return
        }
        this.loadExercises();
    },
    computed: {
        filteredExercises() {
            return this.sortedExercises.filter((exercise) => {
                return exercise.body_part.toLowerCase().match(this.search_bodypart.toLowerCase()) && exercise.exercise_name.toLowerCase().match(this.keyword.toLowerCase()) && exercise.category.toLowerCase().match(this.search_category.toLowerCase())
            })
        
        },
        sortedExercises() {
            return this.exercises.sort((a,b) => {
                let mod = 1;
                if (this.currentSortDir === 'desc') {
                    mod = -1;
                } 
                if (a[this.currentSort] < b[this.currentSort]) {
                    return -1 * mod
                } 
                if (a[this.currentSort] > b[this.currentSort]) {
                    return 1 * mod
                }
                return 0;
            });
        }
    },
    methods: {
        checkHistory(index) {
            // Set index to the exercise you want history of, exerciseHistory has a watcher on this variable.
            this.check_history = this.filteredExercises[index]["exercise_id"];
        },
        resetIndex() {
            // When popup is closed, set index to null (to fix a bug where you couldn't check exercise history of same exercise twice in a row)
            this.check_history = null;
        },
        loadExercises: async function () {
            // GET request 
            let response = await fetch("/resource/" + this.user + "/exercises");
            if (response.status == 200) {
                let result = await response.json();
                if (result) {
                    this.exercises = result;
                }
            }
        },
        loadGlobalExercises: async function() {
            let response = await fetch("/resource/globalexercises");
            if (response.status == 200) {
                let result = await response.json();
                if (result) {
                    this.exercises = result;
                }
            }
        },
        sort(item) {
            if (item === this.currentSort) {
                this.currentSortDir = this.currentSortDir === "asc" ? "desc" : "asc";
            }
            this.currentSort = item;
        },
        createExercise: function (event) {
            // update list with the new exercise, small delay for this.new_exercise_id to be properly updated
            setTimeout(() => {
                this.exercises.push({ userid: this.userid, exercise_id: this.new_exercise_id, exercise_name: event.exercise_name, category: event.category, body_part: event.body_part, global_exercise: 0 });
            }, 150);

        },
        deleteExercise: async function (index) {
            let exercise = this.filteredExercises[index];
            if (!confirm("Are you sure you want to delete this exercise?")) {
                return
            }
            let response = await fetch("/resource/exercise/"+exercise["exercise_id"], {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(exercise)
            });
            if (response.status === 200) {
                let result = await response.json()
                if (result) {
                    // emit alert to indicate success:
                    this.$emit("success", "Exercise '"+exercise["exercise_name"]+"' was deleted")
                    
                    this.loadExercises();
                    
                }
            }
        },
        changeIndexToEdit: function (index) {
            let exercise = this.filteredExercises[index]
            this.indexToEdit = index
            this.editedCategory = exercise["category"];
            this.editedBodyPart = exercise["body_part"];
            
        },
        saveEdit: async function (index) {
            if (this.editedName == "") {
                this.$emit('error', "Give the exercise a name");
                return
            }
            let response = await fetch("/resource/exercise/" + this.filteredExercises[index]["exercise_id"], {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    userid: this.filteredExercises[index]["userid"],
                    exercise_id: this.filteredExercises[index]["exercise_id"],
                    oldName: this.filteredExercises[index]["exercise_name"],
                    newName: this.editedName,
                    oldCategory: this.filteredExercises[index]["category"],
                    newCategory: this.editedCategory,
                    oldBodyPart: this.filteredExercises[index]["body_part"],
                    newBodyPart: this.editedBodyPart
                })
            })
            if (response.status == 200) {
                let result = await response.json();
                if (result) {
                    // finally update list shown on website:
                    this.filteredExercises[index]["exercise_name"] = this.editedName;
                    this.filteredExercises[index]["category"] = this.editedCategory;
                    this.filteredExercises[index]["body_part"] = this.editedBodyPart;
                    
                    this.$emit("success", "Exercise '"+ this.filteredExercises[index]["exercise_name"] +"' was successfully edited");
                    
                    // reset parameters:
                    this.indexToEdit = "";
                    this.editedName = "";
                    this.editedCategory = "";
                    this.editedBodyPart = "";
                    return
                }
                
            }
            
        },
        cancelEdit() {
            this.indexToEdit = "";
            this.editedName = "";
            this.editedCategory = "";
            this.editedBodyPart = "";
            
        },
    }
}