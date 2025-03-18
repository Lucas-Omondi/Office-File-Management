<template>
  <div>
    <h1>User Data</h1>
    <p>{{ userData.name }}</p>
    <p>{{ userData.email }}</p>
  </div>
</template>

<script>
export default {
  name: 'UserComponent',
  data() {
    return {
      userData: null,
    };
  },
  created() {
    // Retrieve data from localStorage when the component is created
    this.userData = JSON.parse(localStorage.getItem('userData'));
  },
};
</script>