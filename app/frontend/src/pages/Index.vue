<template>
  <div class="main">
    <div class="header">
      <div class="title">WSM Search</div>
    </div>
    <div class="search">
      <div class="search-box">
        <Search @search="handleSearch" />
      </div>
    </div>
    <div class="introduction">
      <h3>Introduction:</h3>
      <p>We support different score and filter methods, here are the options you may choose</p>
      <p><b>Score method</b>: Methods used to compute the similarity of query and docs, currently support:</p>
      <div>
        <el-tag class="method" type="info">jaccrd</el-tag>
        <el-tag class="method" type="info">bow</el-tag>
        <el-tag class="method" type="info">tf-idf</el-tag>
      </div>

      <p><b>Filter method</b>: Methods used to filter topk results, currently support:</p>
      <div>
        <el-tag class="method" type="info">heap</el-tag>
        <el-tag class="method" type="info">high-idf</el-tag>
        <el-tag class="method" type="info">multi-terms</el-tag>
        <el-tag class="method" type="info">cluster</el-tag>
      </div>
    </div>
  </div>
</template>

<script>
import Search from "../components/Search";
export default {
  data() {
    return {
      select: "",
      query: ""
    };
  },
  methods: {
    handleSearch(param) {
      if (param.query == "") {
        return;
      }
      this.$router.push("/search/" + param.method + "/" + param.query);
    }
  },
  components: {
    Search
  }
};
</script>

<style scoped>
.main {
  height: 100%;
  width: 100%;
}
.header {
  height: 40%;
  width: 100%;
  background-image: url(../assets/bg.jpg);
  background-size: 100% 100%;
  background-repeat: no-repeat;
  display: flex;
  justify-content: flex-start;
  flex-direction: column-reverse;
  align-items: center;
}
.title {
  color: white;
  font-size: 50px;
  padding: 0;
}
.search-box {
  margin: 0 auto;
  width: 50%;
}
.search {
  padding-top: 90px;
}
.introduction {
  width: 50%;
  margin: 0 auto;
}
.method {
  margin-right: 10px;
}
</style>