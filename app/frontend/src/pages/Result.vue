<template>
  <el-container class="result">
    <el-aside width="130px">
      <WSMSearch />
    </el-aside>
    <el-main>
      <div class="search-box">
        <Search :inputQuery="query" @search="handleSearch"/>
      </div>
      <div class="time">{{timeCost}}</div>
      <div class="result-list" v-loading="loading">
        <ResultItem :item="item" v-for="(item,index) in res" :key="index" />
      </div>
    </el-main>
  </el-container>
</template>

<script>
import Search from "../components/Search";
import ResultItem from "../components/ResultItem";
import WSMSearch from "../components/WSMSearch";
import axios from "axios";

export default {
  created() {
    this.query = this.$route.params.query;
    this.method = this.$route.params.method;
  },
  mounted() {
    this.doSearch();
  },
  data() {
    return {
      loading: true,
      res: [],
      query: "",
      method: "",
      time: ""
    };
  },
  methods: {
    async doSearch() {
      if (this.query == ""){
        return;
      }
      this.loading = true;
      this.time = "";
      let  url = `/search?method=${this.method}&query=${this.query}`
      let res = await axios.get(url);
      if (res.status == 200) {
        if (res.data.status) {
          this.res = res.data.result;
          this.time = res.data.time;
          this.loading = false;
          console.log(this.res);
          console.log(this.time);
        } else {
          this.$message.warn("Unable to search");
        }
      } else {
        this.$message.warn("Network error");
      }
    },
    handleSearch(params){
      this.query = params.query;
      this.method = params.method;
      this.doSearch();
    }
  },
  computed:{
    timeCost(){
      if (this.time == ""){
        return "";
      } else {
        return "Time cost: "+this.time+"s";
      }
    }
  },
  components: {
    Search,
    ResultItem,
    WSMSearch
  }
};
</script>

<style scoped>
.result {
  /* background-color: rgb(245, 245, 245); */
  height: 100%;
}
.title {
  margin: 20px 0 0 10px;
  font-size: 32px;
}
.search-box {
  padding-top: 30px;
  width: 50%;
}
.result-list {
}
.time{
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>