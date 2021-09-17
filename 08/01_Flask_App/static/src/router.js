let router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: [
        { path: '/', component: workoutsC },
        { path: '/new-workout', component: newWorkoutFormC },
        { path: '/all-exercises', component: allExercisesC },
        { path: '/mypage', component: mypageC },
    ]
});

