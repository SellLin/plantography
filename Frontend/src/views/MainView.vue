<template>
  <!--  <div style="display:flex;background-color: rgb(97, 108, 24); padding: 8px; flex-direction: row-reverse">-->
  <div
    style="
      display: flex;
      background-color: #616d17;
      padding: 8px;
      border-radius: 33px;
    "
  >
    <!--    writes icons-->
    <div id="icon" style="display: flex; justify-content: center">
      <svg x="100" width="290" height="200" xmlns="http://www.w3.org/2000/svg">
        <text :transform="textTransform1" :style="textStyle1">
          <tspan :x="tspan1X" :y="tspan1Y" :style="tspan1Style">Pla</tspan>
          <tspan :x="tspan2X" :y="tspan2Y" :style="tspan2Style">n</tspan>
          <tspan :x="tspan3X" :y="tspan3Y" :style="tspan3Style">t</tspan>
          <tspan :x="tspan4X" :y="tspan4Y" :style="tspan4Style">o</tspan>
        </text>
        <text :transform="textTransform2" :style="textStyle2">
          <tspan :x="tspan5X" :y="tspan5Y">g</tspan>
          <tspan :x="tspan6X" :y="tspan6Y" :style="tspan6Style">r</tspan>
          <tspan :x="tspan7X" :y="tspan7Y">aphy</tspan>
        </text>
        <circle
          :cx="circleCX"
          :cy="circleCY"
          :r="circleR"
          :style="circleStyle"
        ></circle>
        <path :d="pathD" :style="pathStyle"></path>
      </svg>
    </div>

    <!--    text area-->
    <div
      style="
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 15vh;
        left: 25px;
        width: 260px;
      "
    >
      <div
        style="
          height: 30px;
          font-family: Montserrat-Bold, serif;
          font-size: 20px;
          font-weight: 600;
          color: white;
          margin-left: 5px;
          margin-top: 13px;
          text-align: start;
        "
      >
        Idea
      </div>
      <el-input
        class="el-textarea__inner"
        type="textarea"
        :autosize="{ minRows: 19, maxRows: 25 }"
        placeholder="Please draw your idea here"
        v-model="textarea2"
      >
      </el-input>
      <button
        @click="get_message"
        style="border-radius: 18px; background: #d8d8b6; height: 35px"
      >
        Generate
      </button>
    </div>

    <div style="z-index: 100">
      <svg
        class="icon"
        viewBox="0 0 1024 1024"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M256 102.4v819.2l512-409.6L256 102.4z"></path>
      </svg>
    </div>

    <div
      style="
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 58vh;
        left: 25px;
        width: 260px;
      "
    >
      <!--      <div class="block">-->
      <!--         <el-slider-->
      <!--      v-model="weather"-->
      <!--      :step="1"-->
      <!--      :show-tooltip="false"-->
      <!--      :min="0"-->
      <!--      :max="3"-->
      <!--      >-->
      <!--    </el-slider>-->
      <!--  </div>-->

      <!--      <div class="slider-container">-->
      <!--  <div class="weather-icon sun">☀️</div>-->
      <!--  <div class="weather-icon cloud">☁️</div>-->
      <!--  <div class="weather-icon rain">🌧️</div>-->
      <!--  <div class="weather-icon snow">❄️</div>-->
      <!--  <input type="range" min="1" max="100" value="50" class="slider" id="myRange">-->
      <!--</div>-->
      <div class="weather-slider" style="border-radius: 6px;">
        <div class="weather-icons">
          <div
            v-for="(icon, index) in weatherIcons"
            :key="icon"
            class="weather-icon"
            :style="{ left: `${iconPositions[index]}%` }"
          >
            <img
              :src="icon"
              :id="'icon' + index"
              alt=""
              height="30"
              width="30"
              class="icon_image"
            />
          </div>
        </div>
        <!--        <div class="icon-container" v-for="(mark, index) in marks" :key="index" :style="{ left: (index * 33.33) + '%' }">-->
        <!--      <img :src="getIconPath(index)" class="weather-icon" alt=""/>-->
        <!--    </div>-->
        <el-slider
          v-model="sliderValue"
          :min="0"
          :max="3"
          :step="1"
          :show-tooltip="false"
          @input="onSliderChange"
          :handle-style="handleStyles"
        />
      </div>

      <div class="weather-slider" style="border-radius: 6px;">
        <!--        <div class="icon-container" v-for="(mark, index) in marks" :key="index" :style="{ left: (index * 33.33) + '%' }">-->
        <!--      <img :src="getIconPath(index)" class="weather-icon" alt=""/>-->
        <!--    </div>-->
        <!--        <div class="tick-mark" v-for="mark in marks" :style="{ left: calculateTickPosition(mark) }"></div>-->
        <el-slider
          v-model="sliderValue1"
          :min="0"
          :max="3"
          :show-tooltip="false"
          :marks="marks"
          @input="onSliderChange1"
        />
        <!--        <div class="tick-mark" v-for="mark in marks" :style="{ left: calculateTickPosition(mark) }"></div>-->
      </div>
      <div class="style-keywords">
        <button class="keyword-btn">Realistic</button>
        <button class="keyword-btn">Cubist</button>
      </div>
      <div class="style-keywords" style="margin-top: 20px">
        <button class="keyword-btn">Watercolor</button>
        <button class="keyword-btn">Ethereal</button>
      </div>
      <div class="style-keywords" style="margin-top: 20px">
        <button class="keyword-btn">Oil painting</button>
        <button class="keyword-btn">Fine details</button>

        <!--      <button class="keyword-btn">...</button>-->
      </div>
      <div
        style="
          height: 30px;
          font-family: Montserrat-Bold, serif;
          font-size: 20px;
          font-weight: 600;
          color: white;
          margin-left: 5px;
          margin-top: 13px;
          text-align: start;
        "
      >
        Example
      </div>

      <el-popover
        trigger="click"
        ref="setRemovePop"
        placement="top"
        :width="160"
      >
        <p>
          A picture of a real landscape with trees including a dogwood and a
          maple.
        </p>
        <div style="text-align: right; margin: 0">
          <!--          <el-button size="small" text @click="cancelRemove()">取消</el-button>-->
          <!--          <el-button size="small" type="primary" @click="cancelRemove()">确定</el-button>-->
        </div>
        <template #reference>
          <el-button
            style="
              position: relative;
              top: 1vh;
              background-color: #858938;
              border: none;
              font-family: Montserrat-Bold, serif;
              font-size: 15px;
              color: white;
            "
          >
            a dogwood and a maple...
          </el-button>
        </template>
      </el-popover>

      <el-popover
        trigger="click"
        ref="setRemovePop"
        placement="top"
        :width="160"
      >
        <p>
          A picture of a real landscape with trees including a dogwood and a
          angelica.
        </p>
        <div style="text-align: right; margin: 0">
          <!--          <el-button size="small" text @click="cancelRemove()">取消</el-button>-->
          <!--          <el-button size="small" type="primary" @click="cancelRemove()">确定</el-button>-->
        </div>
        <template #reference>
          <el-button
            style="
              position: relative;
              top: 2vh;
              left: -12px;
              width: 100%;
              background-color: #858938;
              border: none;
              font-family: Montserrat-Bold, serif;
              font-size: 15px;
              color: white;
            "
          >
            a dogwood and a angelica...
          </el-button>
        </template>
      </el-popover>

      <el-popover
        trigger="click"
        ref="setRemovePop"
        placement="top"
        :width="160"
      >
        <p>A picture of a real landscape with a angelica and a birch.</p>
        <div style="text-align: right; margin: 0">
          <!--          <el-button size="small" text @click="cancelRemove()">取消</el-button>-->
          <!--          <el-button size="small" type="primary" @click="cancelRemove()">确定</el-button>-->
        </div>
        <template #reference>
          <el-button
            style="
              position: relative;
              top: 3vh;
              left: -12px;
              width: 100%;
              background-color: #858938;
              border: none;
              font-family: Montserrat-Bold, serif;
              font-size: 15px;
              color: white;
            "
          >
            A cheery tree in the park...
          </el-button>
        </template>
      </el-popover>
    </div>

    <div>
      <RightView
        :back_data="back_data"
        style="height: calc(100vh - 10px); width: 87vw"
      ></RightView>
    </div>
  </div>
</template>
`

<script>
import RightView from "../components/RightView.vue";
import { inputCaption } from "../service/module/dataService";
import axios from "axios";
import * as d3 from "d3";

export default {
  data() {
    return {
      tspan6Style: {},
      back_data: [],
      weather: 0,
      textTransform1: "translate(54 106.88)",
      textStyle1: {
        fontFamily: "Montserrat-Bold",
        fontSize: "60px",
        fontWeight: "700",
      },
      tspan1X: 0,
      tspan1Y: 0,
      tspan1Style: {
        fontFamily: "Montserrat-Bold",
        fontSize: "60px",
        fontWeight: "700",
        fill: "#ffc215",
      },
      tspan2X: 97.78,
      tspan2Y: 0,
      tspan2Style: {
        fontFamily: "Montserrat-Bold",
        fontSize: "60px",
        fontWeight: "700",
        letterSpacing: "0pt",
        fill: "#ffc215",
      },
      tspan3X: 133.64,
      tspan3Y: 0,
      tspan3Style: {
        fontFamily: "Montserrat-Bold",
        fontSize: "60px",
        fontWeight: "700",
        letterSpacing: "0pt",
        fill: "#ffc215",
      },
      tspan4X: 157.68,
      tspan4Y: 0,
      tspan4Style: {
        fontFamily: "Montserrat-Bold",
        fontSize: "60px",
        fontWeight: "700",
        fill: "#ffffff",
      },
      textTransform2: "translate(135 133.88)",
      textStyle2: {
        fontFamily: "Montserrat",
        fontSize: "31.58px",
        fontWeight: "700",
        fill: "#efefe8",
      },
      tspan5X: 0,
      tspan5Y: 0,
      tspan6X: 21.07,
      tspan6Y: 0,

      tspan7X: 36.89,
      tspan7Y: 0,
      circleCX: 230.07,
      circleCY: 91.26,
      circleR: 10.48,
      circleStyle: {
        fontSize: "16px",
        fill: "#ffffff",
        stroke: "#ffffff",
      },
      pathD:
        "m240.54,83.98c-.44,2.5-1.49,4.96-2.79,7.12-1.05,1.76-2.28,3.64-4.06,4.74-.91.57-2.09,1.01-3.17,1.1-1.56.14-3.14-.24-4.66-.57-.88-.19-1.32.27-1.58,1.08-.16.51.2,1.29.03,1.71-.21.54-.64.65-.95-.03-.43-.94.48-2.61,1.13-3.23-1.06-1.3-1.13-4.26-.65-5.77,1.85-5.73,8.26-7.78,13.7-7.1.25.03,3.08.39,2.98.95h0Z",
      pathStyle: {
        fontFamily: "Times New Roman",
        fontSize: "16px",
        fill: "#979e36",
      },
      textarea2: "",
      visible: false,
      sliderValue: 0,
      sliderValue1: 0,
      weatherIcons: [
        "./src/assets/icon/sun.svg",
        "./src/assets/icon/cloud.svg",
        "./src/assets/icon/rain.svg",
        "./src/assets/icon/snow.svg",
      ], // Replace with the paths to your images
      iconPositions: [1, 30, 60, 90], //[-49, -16, 17, 50] // Position each icon over its corresponding discrete value
      marks: {
        0: "8:00",
        1: "12:00",
        2: "18:00",
        3: "24:00",
      },
    };
  },
  components: { RightView },
  computed: {
    handleStyles() {
      return {
        backgroundColor: this.getHandleColor(this.sliderValue),
        borderColor: this.getHandleColor(this.sliderValue),
      };
    },
  },
  methods: {
    get_message() {
      console.log(this.textarea2);
      let vm = this;
      let path = "http://127.0.0.1:5000/api/test/hello/";
      axios
        .post(path, {
          caption: this.textarea2,
        })
        .then((res) => {
          console.log(res);
          this.back_data = res.data;
          console.log(this.back_data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    onSliderChange(value) {
      // Logic to handle the slider's value change
      d3.selectAll(".icon_image").attr("width", 30).attr("height", 30);
      d3.select("#icon" + value)
        .attr("width", 45)
        .attr("height", 45);
    },
    getIconPath(index) {
      // Return the path to the icon based on the index
      return this.icons[index];
    },
    getHandleColor(value) {
      switch (value) {
        case "0":
          return "#f7ac57"; // color for 8:00
        case "1":
          return "#fffb00"; // color for 12:00
        case "2":
          return "#b0d941"; // color for 18:00
        case "3":
          return "#29aae1"; // color for 24:00
        default:
          return "#fff"; // default color
      }
    },
    calculateTickPosition(mark) {
      // Assuming a linear distribution of marks, calculate position as a percentage
      const totalMarks = Object.keys(this.marks).length - 1;
      const position = (mark / totalMarks) * 100;
      return `${position}%`;
    },
  },
};
</script>

<style>
.el-textarea__inner {
  background-color: #858938 !important;
  box-shadow: 0 0 0 0;
  padding: 4px;
  color: white;
  font-family: Montserrat, serif;
  font-size: 14px;
}

.icon {
  fill: #858938;
  position: absolute;
  top: 36vh;
  left: -37px;
  width: 80px;
  height: 100px;
}
</style>

<style scoped>
.weather-slider /deep/ .el-slider__runway {
  /* Remove the default background styling */
  background: none;
  height: 6px; /* Your desired track height */
  border-radius: 3px; /* Half of the height to make it rounded */
}

.weather-slider /deep/ .el-slider__bar {
  /* Hide the default filled part of the slider */
  display: none;
}

.weather-slider /deep/ .el-slider__runway:before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: linear-gradient(
    to right,
    #f7ac57,
    #fffb00 25%,
    #b0d941 50%,
    #29aae1 75%,
    #0d4f8b
  );
  border-radius: 3px; /* Match the runway's border-radius */
}

.weather-slider /deep/ .el-slider__button {
  /* Custom styling for the slider thumb (optional) */
  background-color: #fff;
  border: 2px solid #ccc;
}
.weather-slider {
  position: relative;
  width: 100%; /* Adjust as needed */
  padding-top: 30px; /* Space for icons */
}

.weather-icons {
  position: absolute;
  width: 100%;
  top: -17px;
  pointer-events: none; /* Ensures clicks pass through to the slider below */
}

.weather-icon {
  position: absolute;
  transform: translateX(-50%); /* Center the icons above the slider */
}
.tick-mark {
  position: absolute;
  top: -10px; /* Adjust as necessary to position above the slider */
  width: 2px; /* Width of the tick mark */
  height: 10px; /* Height of the tick mark */
  background-color: #000; /* Color of the tick mark */
  /* More styling as needed */
}
.weather-slider /deep/ .el-slider__button {
  /* Other styles */
}

.weather-slider /deep/ .el-slider__marks-text {
  transform: translateX(-50%);
  color: #ffffff;
}

.weather-slider /deep/ .el-slider__marks {
  width: 90%;
  display: flex;
  top: -40px;
  color: #ffffff;
  justify-content: space-between;
}

.weather-slider /deep/ .el-slider__mark {
  flex: none;
}
.weather-slider /deep/ .el-slider__step {
  display: block;
  position: absolute;
  height: 6px; /* Match the height of the runway */
  background: #fff; /* This should be transparent or the color of the step mark */
  z-index: 1; /* Ensure the step is above the runway */
}

/* Adjust the size and position of the step marks */
.weather-slider /deep/ .el-slider__step.active {
  width: 2px;
  height: 10px; /* Height of the active step mark */
  background: currentColor; /* Color of the active step mark, use a CSS variable or class to change per step */
  margin-top: -2px; /* Adjust as necessary */
}

/* Optional: Add a transition effect when the slider value changes */
.weather-slider /deep/ .el-slider__button-wrapper {
  transition: left 0.3s ease-in-out;
}

.weather-slider {
  position: relative;
  margin-top: 14px; /* Adjust if necessary to make space for time labels */
  padding: 10px; /* Add padding to create space around the slider */
  background-color: #858938; /* Replace with the actual hex code for the shallow green color you want */
  border-radius: 10px; /* Adjust as needed to match the design in the image */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Optional: adds a subtle shadow for depth */
}
.style-keywords {
  display: flex;
  justify-content: space-around; /* Distribute buttons evenly */
  //position: absolute; /* Absolute positioning within the .weather-slider container */
  bottom: 10px; /* Adjust as needed to position at the bottom of the .weather-slider */
  left: 0;
  right: 0;
  margin-top: 30px;
}

.keyword-btn {
  padding: 5px 10px; /* Adjust padding for buttons */
  font-size: 12px; /* Adjust font size as needed */
  background-color: #858938; /* Button background color */
  color: #ffffff; /* Button text color */
  border: none;
  width: 120px;
  border-radius: 15px; /* Adjust to match your design */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Optional: adds subtle shadow to buttons */
  cursor: pointer;
}

.keyword-btn:not(:last-child) {
  margin-right: 5px; /* Spacing between buttons, adjust as needed */
}

/* Additional styling for hover effects, active state, etc., if desired */
.keyword-btn:hover {
  background-color: #858938;
}
</style>

<!--<style scoped>-->
<!--.weather-slider /deep/ .el-slider__marks {-->
<!--  display: none; /* Hide the default labels */-->
<!--}-->

<!--.weather-slider /deep/ .el-slider__marks .el-slider__marks-text {-->
<!--  position: absolute;-->
<!--  width: 10px; /* Circle size */-->
<!--  height: 10px; /* Circle size */-->
<!--  border: 2px solid grey; /* Circle border color */-->
<!--  border-radius: 50%; /* Make it round */-->
<!--  background: grey; /* Circle fill color */-->
<!--  top: -14px; /* Adjust vertical position */-->
<!--  transform: translateX(-50%); /* Center the circle on the mark */-->
<!--}-->

<!--.weather-slider /deep/ .el-slider__dot {-->
<!--  /* Optional: Style the dots that appear when the slider is hovered or focused */-->
<!--  background-color: grey;-->
<!--  border-color: grey;-->
<!--}-->

<!--.weather-slider /deep/ .el-slider__button {-->
<!--  /* Optional: Style the button to match the design */-->
<!--  background-color: white;-->
<!--  border: 2px solid grey;-->
<!--}-->
<!--</style>-->
