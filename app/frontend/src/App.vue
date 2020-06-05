<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
}

body {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  background-color: rgb(245,245,245);
}

html {
  width: 100%;
  padding: 0;
  height: 100%;
}
</style>
