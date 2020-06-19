<template>
  <el-autocomplete
    :fetch-suggestions="querySearchAsync"
    placeholder="Enter your query here"
    @keyup.enter.native="handleSearch"
    v-model="query"
    :trigger-on-focus="false"
    :maxlength="20"
    show-word-limit
    class="input-box"
  >
    <el-select class="select" v-model="method" slot="prepend" placeholder="Search Method">
      <el-option v-for="(m,i) in method_list" :key="i" :label="m.label" :value="m.value"></el-option>
    </el-select>
    <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
  </el-autocomplete>
  <!-- <el-input placeholder="Enter your query here" @keyup.enter.native="handleSearch" v-model="query">
    <el-select class="select" v-model="method" slot="prepend" placeholder="Search Method">
      <el-option v-for="(m,i) in method_list" :key="i" :label="m.label" :value="m.value"></el-option>
    </el-select>
    <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
  </el-input>-->
</template>

<script>
import axios from "axios";
export default {
  props: ["inputQuery", "inputMethod"],
  mounted() {
    if (this.$props.inputQuery) {
      this.query = this.$props.inputQuery;
    }
    if (this.$props.inputMethod) {
      this.method = this.$props.inputMethod;
    }
    let score = ["tf-idf", "jaccard", "bow"];
    let filter_type = ["cluster", "high-idf", "multi-terms","heap"];
    let methods = [];
    for (let i = 0; i < score.length; i++)
      for (let j = 0; j < filter_type.length; j++)
        methods.push({
          label: score[i] + "+" + filter_type[j],
          value: score[i] + "," + filter_type[j]
        });
    this.method_list = methods;
  },
  data() {
    return {
      method: "tf-idf,cluster",
      query: "",
      method_list: []
    };
  },
  computed: {
    init_query() {
      return this.$props.inputQuery;
    }
  },
  watch: {
    init_query(to, from) {
      console.log(from);
      this.query = to;
    }
  },
  methods: {
    querySearchAsync(queryString, cb) {
      console.log(queryString);
      axios.get("/suggestion?query=" + queryString).then(res => {
        console.log(res);
        if (res.status == 200) {
          if (res.data.status == 1) {
            console.log(res.data.queries);
            cb(res.data.queries.slice(0, 5));
          }
        }
      });
    },
    handleSearch() {
      if (this.query == "") {
        return;
      }

      this.$emit("search", {
        query: this.query.substr(0, 20),
        method: this.method
      });
    }
  }
};
</script>

<style>
.select {
  width: 150px;
}
.input-box {
  width: 600px;
}
</style>