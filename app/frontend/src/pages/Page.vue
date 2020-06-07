<template>
  <el-container class="page">
    <el-aside width="130px">
      <WSMSearch />
    </el-aside>
    <el-main>
      <div class="title">
        <h2>{{title}}</h2>
        <el-link class="link" :href="url" type="primary">Access Origin Page</el-link>
      </div>
      <div class="body">
        <p v-for="(p,index) in content" :key="index">{{p}}</p>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import WSMSearch from "../components/WSMSearch";
import Axios from "axios";
export default {
  async mounted() {
    let res = await Axios.get("/page?id=" + this.$route.params.id);
    if (res.status == 200) {
      if (res.data.status == 1) {
        this.title = res.data.page.title;
        this.text = res.data.page.text;
        this.url = res.data.page.url;
      } else {
        this.$message.warn("Can not load page");
      }
    } else {
      this.$message.warn("Network error");
    }
  },
  data() {
    return {
      title: "",
      text: "",
      url: ""
    };
  },
  computed:{
    content(){
      let text = this.text;
      if (text.startsWith(this.title)){
          text = text.substring(this.title.length);
      }
      text = text.split("\n");
      return text;
    }
  },
  components: {
    WSMSearch
  }
};
</script>

<style scoped>
.page {
  height: 100%;
}
.title {
  font-size: 32px;
}
.body {
  font-size: 18px;
  line-height: 30px;
  text-indent: 36px;
}
.link {
  margin-top: -40px;
  font-size: 18px;
}
</style>