<template>
  <!--  <div style="display:flex;background-color: rgb(238, 238, 232); padding: 15px">-->
  <div style="display:flex;background-color: #efefe8; padding: 5px; border-radius: 27px;">
    <div>
      <GraphView :graphData="graphData" class="view" style="height:calc(40vh - 25px);" @new_box="new_box"></GraphView>
      <br>
      <LayoutView :layoutData="layoutData" ref="layoutView" class="view" style="height:calc(60vh - 25px);"></LayoutView>
    </div>


    <ResultView class="view" style="height:calc(100vh - 40px);width:55vw"></ResultView>

  </div>
</template>

<script>
import GraphView from "../components/GraphView.vue"
import LayoutView from "../components/LayoutView.vue"
import ResultView from "../components/ResultView.vue"

export default {
  props: ['back_data'],
  data() {
    return {
      graphData: [],
      layoutData: []
    }
  },
  watch: {
    back_data: function (val) {
      console.log(val)
      this.graphData = val['sc']
      this.layoutData = val['ro']
      console.log(this.graphData)

    }
  },
  methods: {
    new_box(addType){
      console.log("addNode")
      console.log(addType)
      this.$refs.layoutView.addBox(addType)
    }
  },
  components: {GraphView, LayoutView, ResultView}
}
</script>

<style>
.view {
  width: 30vw;
  margin-left: 10px;
  margin-right: 5px;
  margin-bottom: 10px;
  border-radius: 18px;
}


</style>