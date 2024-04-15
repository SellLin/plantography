<template>
  <div style="height: 100%;">


    <!--    graph -->
    <div
        style="background: #d8d8b6; float: right; position:absolute; top: 2%; left: 0; width: 100%; border-radius: 18px; height: 5vh;">
      <div style="background: none">
        <el-button class="button" @click="open()">Render</el-button>
      </div>


      <!--  main  graph-->
    </div>
    <div style="background: #ffffff; height: calc(89vh - 3px); border-radius: 18px; position: relative; top: 8vh; box-shadow: 10px 4px 16px rgba(0, 0, 0, 0.3);">
     <div style="width:90%;height:80%;margin-left: 4%"> <img v-if="showImage" :src="imageSrc" alt=" " style="width:100%;height:100%;"> </div>
      <div
            style="height: 30px; margin-left: 50px; font-family: Montserrat-Bold,serif; font-size:26px; font-weight:600; color: rgb(97 108 24); margin-top: 13px; text-align: start;">
          History
        </div>

      <div>
        <img v-for="(path, index) in history" :src="path" alt=" " style="float:left; width:130px;height:130px; margin-left: 50px; margin-top: 10px; margin-right: 10px; border-radius: 10px; border: 1px solid #d8d8b6;">
      </div>
    </div>

  </div>
</template>


<script>

export default {
  data() {
    return {
      showImage: false,
      imageSrc: null,
      counter: 0,
      history: [],
    }
  },
  methods: {
    open() {
      try {

        this.imageSrc = "./src/assets/result/image_crepen_tulip_" + this.counter + ".png";
        this.history.push(this.imageSrc)
        this.counter +=1;
        // this.imageSrc = "./src/assets/result/image_crepen_tulip_0.png";
        this.showImage = true;
      } catch (error) {
        console.log(error);
      }
    }
  }
}
</script>

<style>
.button {
  height: 100%;
  width: 100%;
  font-family: Montserrat-Bold, serif;
  font-size: 25px;
  font-weight: 800;
  color: rgb(97 108 24);
//margin-left: 25px; margin-top: 14px;
  text-align: left;
  padding-left: 25px;
  display: block;
  background: none;
  border: none;
}

.cls-1 {
  fill: #adad73;
}

.cls-2 {
  fill: #efefe8;
}

.cls-3 {
  fill: #ffc215;
}


</style>