const mypageC = {
    props: ["user", "role", "email", "userid", "new_exercise_id"],
    emits: ["new-exercise", "error", "success", "user-loggedout"],
    template: /*html*/`
    <div>
        <h1>Your Details</h1>
        <div class="accent-container">
            <div class="table-style">
                <table class="mypage-table">
                    <tr>
                        <td>Username:</td>
                        <td>{{ user }}</td>
                        
                    </tr>
                    <tr>
                        <td>Email:</td>
                        <td>{{ email }}</td>
                        
                    </tr>
                    <tr>
                        <td>Role:</td>
                        <td>{{ role }} user</td>
                    </tr>
                    
                </table>
                <br>
                <p v-if="role!=='admin'" class="self-destruct" v-on:click="deleteUser">Self Destruct</p>
            </div>
        </div>
        
        <h2>BMI Calculator</h2>
        <div class="accent-container">
            <form class="table-style bmi-calc">
                <table class="mypage-table">
                    <tr colspan="2">
                        <th>Weight: </th>
                        <td><input class="inputs" type="text" v-model="weight"> kg</td>
                        <th id="more-space">Gender: </th>
                        <td>
                        <input type="radio" value="male" id="male" name="gender" v-model="gender">&nbsp<label for="male">Male</label>&nbsp
                        <input type="radio" value="female" id="female" name="gender" v-model="gender">&nbsp<label for="female">Female</label>
                        </td>
                    </tr>
                    <tr>
                        <th>Height: </th>
                        <td id="no-newline"><input class="inputs" type="text" v-model="height"> cm</td>
                        <th id="more-space">Age: </th>
                        <td><input class="inputs" type="text" v-model="age"> years old</td>
                    </tr>
                    <tr colspan="1">
                        <td></td>
                        <td></td>
                        <th id="more-space">Activity level: </th>
                        <td>
                            <select class="inputs" style="width: 100%; font-size:normal;" v-model="activity">
                                <option value="1.2">Little or no</option>
                                <option value="1.375">Lightly active</option>
                                <option value="1.55">Moderate active</option>
                                <option value="1.725">Hard exercise (6-7 days/week)</option>
                                <option value="1.9">Very hard exercise & physical job</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th>BMI: </th>
                        <td>{{ bmi }}</td>
                        <th id="more-space">Calorie maintenance: </th>
                        <td>{{ calories }} kcal</td>
                    </tr>
                    
                </table>
            </form>
        </div>

        <admin-page v-if="role=='admin'"
        v-on:new-exercise="$emit('new-exercise', $event)"
        v-on:error="$emit('error', $event)"
        v-on:success="$emit('success', $event)"
        v-bind:new_exercise_id="new_exercise_id"
        v-bind:userid="userid"
        v-bind:user="user"
        
        ></admin-page>
    </div>
    `,
    data() {
        return {
            weight: "",
            height: "",
            bmi: "",
            gender: "",
            age: "",
            activity: "",
            calories: 0,
        }
    },
    watch: {
        weight: function() {
            this.bmi = Math.round((this.weight / (this.height/10)**2)*100*100)/100;
            this.calorieMaintenance();
 
        },
        height: function() {
            this.bmi = Math.round((this.weight / (this.height/10)**2)*100*100)/100;
            this.calorieMaintenance();

        },
        age() {
            this.calorieMaintenance();
        },
        gender() {
            this.calorieMaintenance();
        },
        activity() {
            this.calorieMaintenance();
        }

    },
    methods: {
        calorieMaintenance() {
            if (this.gender === "male") {
                let bmr =  10*this.weight+6.25*this.height-5*this.age+5; 
                this.calories = Math.round(bmr * this.activity);
            } else if (this.gender === "female") {
                let bmr = 10*this.weight+6.25*this.height-5*this.age-161;
                this.calories = Math.round(bmr * this.activity);

            }
        },
        deleteUser: async function() {
            if (!confirm("Are you sure you want to delete your account along with all exercises and recorded workouts?")) {
                return
            }
            let response = await fetch("/user/"+this.userid, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                }
            });
            if (response.status == 200) {
                let result = await response.text()
                if (result) {                    
                    this.$emit('success', "Account deleted");
                    this.$emit('user-loggedout');
                    return
                } 
                this.$emit('error', "Something went wrong...");
        
            }
        }
    }

}