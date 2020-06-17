<template>
  <div class="result-item">
    <el-link @click="goto" class="title" :type="titleColor" v-html="title"></el-link>
    <p class="abstract" v-html="abstract"></p>
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
    },
    title() {
      let res = this.$props.item.title;
      for (let i = 0; i < this.$props.item.words.length; i++) {
        let word = this.$props.item.words[i];
        res = res.replace(word, `<span style="color:#F56C6C;">${word}</span>`);
      }
      return res;
    },
    abstract() {
      let res = this.$props.item.abstract;
      for (let i = 0; i < this.$props.item.words.length; i++) {
        let word = this.$props.item.words[i];
        res = res.replace(word, `<span style="color:#F56C6C;">${word}</span>`);
      }
      return res;
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