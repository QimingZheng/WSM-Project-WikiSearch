<template>
  <div class="main">
    <div class="header">
      <div class="title">WSM Search</div>
    </div>
    <div class="search">
      <div class="search-box">
        <Search/>
      </div>
    </div>
  </div>
</template>

<script>
import Search from "../components/Search"
export default {
  data() {
    return {
      select: "",
      query: ""
    };
  },
  methods: {
    handleSearch() {
      if (this.query == "") {
        return;
      }
      this.$router.push("/search/" + this.query);
    }
  },
  components:{
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
  padding-top: 100px;
}
</style>