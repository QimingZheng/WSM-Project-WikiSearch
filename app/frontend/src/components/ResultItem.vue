<template>
  <div class="result-item">
    <el-link @click="goto" class="title" :type="titleColor">{{item.title}}</el-link>
    <p class="abstract">{{item.abstract}}</p>
  </div>
</template>

<script>
export default {
  props: ["item"],
  data() {
    return {};
  },
  computed: {
    titleColor() {
      return "primary";
    }
  },
  methods: {
    goto() {
      this.$router.push("/page/" + this.item.id);
    }
  }
};
</script>

<style scoped>
.result-item {
  margin-top: 20px;
  padding-bottom: 10px;
}
.title {
  font-size: 18px;
}
.abstract {
}
</style>