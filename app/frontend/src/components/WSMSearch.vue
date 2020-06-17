<template>
  <p class="title" @click="goBack">
    WSM
    <br />Search
  </p>
</template>

<script>
export default {
  methods: {
    goBack() {
      this.$router.push("/index");
    }
  }
};
</script>

<style scoped>
.title {
  margin: 20px 0 0 10px;
  font-size: 32px;
  cursor: pointer;
}
</style>