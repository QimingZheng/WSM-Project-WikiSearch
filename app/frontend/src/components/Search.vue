<template>
  <el-input placeholder="Enter your query here" @keyup.enter.native="handleSearch" v-model="query">
    <el-select class="select" v-model="method" slot="prepend" placeholder="Search Method">
      <el-option label="method1" value="test"></el-option>
      <el-option label="method2" value="2"></el-option>
      <el-option label="method3" value="3"></el-option>
    </el-select>
    <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
  </el-input>
</template>

<script>
export default {
  props: ["inputQuery"],
  mounted() {
    if (this.$props.inputQuery) {
      this.query = this.$props.inputQuery;
    }
  },
  data() {
    return {
      method: "test",
      query: ""
    };
  },
  methods: {
    handleSearch() {
      if (this.query == "") {
        return;
      }
      this.$emit("search",{
        query:this.query,
        method:this.method
      })
    }
  }
};
</script>

<style>
.select {
  width: 150px;
}
</style>