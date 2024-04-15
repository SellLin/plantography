<template>
  <div style="height: 100%;">
    <!--    buttons-->
    <div
      style="
        position: absolute;
        top: 29%;
        left: 0;
        width: 50px;
        background: #efefe8;
      "
    >
      <div
        style="
          background: none;
          display: flex;
          flex-direction: column;
          align-content: flex-start;
          justify-content: center;
          align-items: flex-start;
        "
      >
        <!--       Graph Buttons -->
        <!--              <el-row>-->
        <button class="svg-button-1" @click="open()">
          <svg
            id="arrow"
            viewBox="0 0 41.72 32.14"
            transform="translate(4.1 0)"
          >
            <path
              class="cls-1"
              d="M22.72,22.72l-6.65-6.65L0,0v32.14l9.41-9.42h13.31Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->

        <!--              <el-row>-->
        <button class="svg-button-1" @click="changeLayout()">
          <svg id="add" viewBox="0 0 44.72 32.14">
            <path
              class="cls-1"
              d="M23.33,29.33H6c-3.31,0-6-2.69-6-6V6C0,2.69,2.69,0,6,0h17.33c3.31,0,6,2.69,6,6v17.33c0,3.31-2.69,6-6,6ZM14.66,8.24c-.59,0-1.07.48-1.07,1.07v4.28h-4.28c-.59,0-1.07.48-1.07,1.07s.48,1.07,1.07,1.07h4.28v4.28c0,.59.48,1.07,1.07,1.07s1.07-.48,1.07-1.07v-4.28h4.28c.59,0,1.07-.48,1.07-1.07s-.48-1.07-1.07-1.07h-4.28v-4.28c0-.59-.48-1.07-1.07-1.07Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->

        <!--              <el-row>-->
        <button class="svg-button-1" @click="open()">
          <svg id="reduce" viewBox="0 0 44.72 32.14">
            <path
              class="cls-1"
              d="M23.33,29.33H6c-3.31,0-6-2.69-6-6V6C0,2.69,2.69,0,6,0h17.33c3.31,0,6,2.69,6,6v17.33c0,3.31-2.69,6-6,6Zm-3.35-15.73h-10.63c-.48,0-.88.39-.88.88v.39c0,.48.39.88.88.88h10.63c.48,0,.88-.39.88-.88v-.39c0-.48-.39-.88-.88-.88Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->

        <!--              <el-row>-->
        <button class="svg-button-1" @click="drawForce(layoutData)">
          <svg id="refresh" viewBox="0 0 44.72 32.14">
            <rect class="cls-1" width="29.33" height="29.33" rx="6" ry="6" />
            &ndash;&gt;-->
            <path
              class="cls-2"
              d="M14.66,9.51v-3.26l-4.08,4.08,4.08,4.08v-3.26c2.7,0,4.89,2.19,4.89,4.89s-2.19,4.89-4.89,4.89-4.89-2.19-4.89-4.89h-1.63c0,3.61,2.92,6.53,6.53,6.53s6.53-2.92,6.53-6.53c0-3.61-2.92-6.53-6.53-6.53Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->
      </div>
    </div>

    <!--    graph -->
    <div
      style="
        background: #ffffff;
        float: right;
        position: absolute;
        top: 5%;
        right: 9px;
        width: calc(100% - 50px);
        border-radius: 18px;
        box-shadow: 10px 4px 16px rgba(0, 0, 0, 0.3);
      "
    >
      <div>
        <div
          style="
            height: 30px;
            font-family: Montserrat-Bold, serif;
            font-size: 20px;
            font-weight: 600;
            color: rgb(97 108 24);
            margin-left: 25px;
            margin-top: 13px;
            text-align: start;
          "
        >
          Layout
        </div>

        <!--  main  graph-->
        <div style="background: #ffffff; height: 52vh; border-radius: 18px; overflow: hidden; box-sizing: border-box; padding: 14px; margin-left: 9px">
          <svg
            ref="layoutView"
            style="width: 100%; height: 100%; border: 1px solid #f0f0f0; border-radius: 18px;"
            id="layoutBox"
          >
<!--            <rect x="10" y="10" width="calc(100% - 45px)" height="calc(100% - 33px)" fill="none" stroke="#f0f0f0" stroke-width="1" />-->
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { postImgSeg, postLayout } from "../service/module/dataService";
export default {
  data() {
    return {
      dragF: null,
      dragF1: null,
      dragStartX: 0,
      dragStartY: 0,
      dragStartX1: 0,
      dragStartY1: 0,
      scaleState: 0,
      scaleState1: 0,
      prevX: 0,
      prevY: 0,
      prevX1: 0,
      prevY1: 0,
      format_data: null,
      translateX: 0,
      translateY: 0,
      boxCount: 0,
      colors: null,
    };
  },
  watch: {
    layoutData: function (val) {
      console.log(val);
    },
  },
  props: {
    objs: {
      type: Array,
      default: () => [
        "bougainvillea",
        "poinciane",
        "dogwood",
        "bush",
        "alumroot",
      ],
    },
    triples: {
      type: Array,
      default: () => [
        { source: 0, target: 1 },
        { source: 1, target: 3 },
        { source: 0, target: 3 },
        { source: 2, target: 0 },
        { source: 4, target: 2 },
      ],
    },
    outputFolder: String,
    imageId: String,
    layoutData: Array,
  },
  methods: {
    generateRandomWarmColor() {
      const r = Math.floor(Math.random() * 156); // 0 to 155
      const g = 100 + Math.floor(Math.random() * 56); // 100 to 155
      const b = 100 + Math.floor(Math.random() * 56); // 100 to 155
      const alpha = 0.2;
      return `rgba(${r},${g},${b},${alpha})`;
    },

    drawForce(layout_data) {
      console.log(layout_data);
      let formatted_data = layout_data.map((d) => ({
        name: d[0],
        coords: d[1],
      }));
      this.format_data = formatted_data;
      this.dragF = d3
        .drag()
        .on("start", dragStart) // 拖动开始，触发一次
        .on("drag", draged) // 拖动中，触发多次
        .on("end", dragEnd) // 拖动结束，触发一次
        .container(d3.select("#layoutBox"));
      let dragStartX = this.dragStartX;
      let dragStartY = this.dragStartY;
      let scaleState = this.scaleState;
      let thi = this;
      function dragStart(event) {
        // console.log("dragStart")
        // console.log(d3.select(this).attr("startX"))
        // console.log(event.x)
        // console.log(event.x+Number(d3.select(this).attr("startX")))
        //  d3.select(this).attr("x",event.x).attr("y",event.y)
        dragStartX = event.x;
        dragStartY = event.y;
        thi.prevX = event.x;
        thi.prevY = event.y;
        //d3.select(this).attr("x",event.x+Number(d3.select(this).attr("startX"))).attr("y",event.y+Number(d3.select(this).attr("startY")))
      }

      function draged(event) {
        if (thi.scaleState == 0) {
          d3.select(this)
            .attr(
              "x",
              event.x - dragStartX + Number(d3.select(this).attr("startX"))
            )
            .attr(
              "y",
              event.y - dragStartY + Number(d3.select(this).attr("startY"))
            );
          // d3.select(this).attr("x",event.x).attr("y",event.y)
          d3.select("#rectText" + d3.select(this).attr("rect_id"))
            .attr(
              "x",
              10 + event.x - dragStartX + Number(d3.select(this).attr("startX"))
            )
            .attr(
              "y",
              20 + event.y - dragStartY + Number(d3.select(this).attr("startY"))
            );
        } else {
          if (event.x - dragStartX > 0) {
            d3.select(this).attr(
              "width",
              Number(d3.select(this).attr("width")) + (event.x - thi.prevX)
            );
          } else {
            d3.select(this).attr(
              "width",
              Number(d3.select(this).attr("width")) + (event.x - thi.prevX)
            );
            // d3.select(this).attr("x", Number(d3.select(this).attr("x"))+event.x - dragStartX)
          }
          if (event.y - dragStartY < 0) {
            d3.select(this).attr(
              "height",
              Number(d3.select(this).attr("height")) + (event.y - thi.prevY)
            );
          } else {
            d3.select(this).attr(
              "height",
              Number(d3.select(this).attr("height")) + (event.y - thi.prevY)
            );
            // d3.select(this).attr("y", Number(d3.select(this).attr("y"))+event.y - dragStartY)
          }
          thi.prevX = event.x;
          thi.prevY = event.y;
        }
      }
      function dragEnd(event) {
        console.log("dragEnd");
        d3.select(this).attr("startX", d3.select(this).attr("x"));
        d3.select(this).attr("startY", d3.select(this).attr("y"));
      }
      //开始布局画图
      const svg = d3.select(this.$refs.layoutView);
      const canvasWidth = svg.node().getBoundingClientRect().width;
      const canvasHeight = svg.node().getBoundingClientRect().height;

      // Compute combined dimensions of all bounding boxes
      const minX = d3.min(formatted_data, (d) => d.coords[0]);
      const minY = d3.min(formatted_data, (d) => d.coords[1]);
      const maxX = d3.max(formatted_data, (d) => d.coords[0] + d.coords[2]);
      const maxY = d3.max(formatted_data, (d) => d.coords[1] + d.coords[3]);

      const combinedWidth = maxX - minX;
      const combinedHeight = maxY - minY;

      // Compute translation for centering
      const translateX = (canvasWidth - combinedWidth) / 2 - minX;
      const translateY = (canvasHeight - combinedHeight) / 2 - minY;
      this.translateX = translateX;
      this.translateY = translateY;
      svg.selectAll("*").remove(); // Clear previous drawings

      // //定义一个序数颜色比例尺
      var color = d3.scaleOrdinal(d3.schemeCategory10);
      this.colors = color;

      this.boxCount = formatted_data.length;

      svg
        .selectAll("rect")
        .data(formatted_data)
        .enter()
        .append("rect")
        .attr("x", (d) => d.coords[0] + translateX)
        .attr("y", (d) => d.coords[1] + translateY)
        .attr("startX", (d) => d.coords[0] + translateX)
        .attr("startY", (d) => d.coords[1] + translateY)
        .attr("width", (d) => d.coords[2])
        .attr("height", (d) => d.coords[3])
        .attr("id", (d, i) => "rect" + i)
        .attr("class", "layoutRect")
        .attr("name", (d) => d.name)
        .attr("rect_id", (d, i) => i)
        .attr("fill-opacity", 0.2)
        .attr("fill", (d, i) => {
          return color(i);
        })
        .attr("stroke", (d, i) => {
          return color(i);
        })
        .attr("rx", "10") // half of the previous radius value to make it more rounded
        .attr("ry", "10")
        .attr("stroke-width", "2")
        // .on("dblclick", function(){
        //   if (thi.scaleState==0)
        //   {
        //     d3.select("rect"+d3.select(this).attr("text_id")).attr("stroke-width", 4)
        //     thi.scaleState=1
        //   }
        //   else
        //   {
        //     d3.select("rect"+d3.select(this).attr("text_id")).attr("stroke-width", 2)
        //     thi.scaleState=0
        //   }
        // })
        .on("dblclick", function () {
          if (thi.scaleState == 0) {
            d3.select(this).attr("stroke-width", 6);
            thi.scaleState = 1;
          } else {
            d3.select(this).attr("stroke-width", 2);
            thi.scaleState = 0;
          }
        })
        .call(this.dragF);

      svg
        .selectAll("text")
        .data(formatted_data)
        .enter()
        .append("text")
        .attr("x", (d) => d.coords[0] + translateX + 10)
        .attr("y", (d) => d.coords[1] + translateY + 20)
        .attr("id", (d, i) => "rectText" + i)
        .attr("text_id", (d, i) => i)
        .attr("font-size", "14")
        .attr("fill", "black")
        .text((d) => d.name);
    },
    changeLayout() {
      let allRects = d3.selectAll(".layoutRect");
      console.log("changeLayout");
      console.log(allRects._groups[0]);
      let layoutList = [];
      let layoutStr = "";
      for (let i = 0; i < allRects._groups[0].length; i++) {
        console.log(allRects._groups[0][i].attributes["x"]["value"]);
        console.log(allRects._groups[0][i].attributes["width"]["value"]);
        let x =
          Number(allRects._groups[0][i].attributes["x"]["value"]) -
          this.translateX -
          10;
        let y =
          Number(allRects._groups[0][i].attributes["y"]["value"]) -
          this.translateY -
          20;
        let width = Number(allRects._groups[0][i].attributes["width"]["value"]);
        let height = Number(
          allRects._groups[0][i].attributes["height"]["value"]
        );
        let name = allRects._groups[0][i].attributes["name"]["value"];
        layoutList.push({ name: name, layout: [x, y, width, height] });
        layoutStr =
          layoutStr +
          name +
          "," +
          x +
          "," +
          y +
          "," +
          width +
          "," +
          height +
          ";";
      }
      console.log(layoutList);
      let layoutObj = { layout: layoutList };
      let formData = new FormData();
      formData.append("layoutStr", layoutStr);
      postLayout(formData, (res) => {
        console.log(res);
      });
    },
    addBox(name) {
      let allRects = d3.selectAll(".layoutRect");
      let rectCounts = allRects._groups[0].length;
      let svg = d3.select(this.$refs.layoutView);
      this.dragF1 = d3
        .drag()
        .on("start", dragStart) // 拖动开始，触发一次
        .on("drag", draged) // 拖动中，触发多次
        .on("end", dragEnd) // 拖动结束，触发一次
        .container(d3.select("#layoutBox"));
      let dragStartX1 = this.dragStartX1;
      let dragStartY1 = this.dragStartY1;
      let scaleState1 = this.scaleState1;
      let thi = this;
      function dragStart(event) {
        // console.log("dragStart")
        // console.log(d3.select(this).attr("startX"))
        // console.log(event.x)
        // console.log(event.x+Number(d3.select(this).attr("startX")))
        //  d3.select(this).attr("x",event.x).attr("y",event.y)
        dragStartX1 = event.x;
        dragStartY1 = event.y;
        thi.prevX1 = event.x;
        thi.prevY1 = event.y;
        //d3.select(this).attr("x",event.x+Number(d3.select(this).attr("startX"))).attr("y",event.y+Number(d3.select(this).attr("startY")))
      }

      function draged(event) {
        if (thi.scaleState1 == 0) {
          d3.select(this)
            .attr(
              "x",
              event.x - dragStartX1 + Number(d3.select(this).attr("startX"))
            )
            .attr(
              "y",
              event.y - dragStartY1 + Number(d3.select(this).attr("startY"))
            );
          // d3.select(this).attr("x",event.x).attr("y",event.y)
          d3.select("#rectText" + d3.select(this).attr("rect_id"))
            .attr(
              "x",
              10 +
                event.x -
                dragStartX1 +
                Number(d3.select(this).attr("startX"))
            )
            .attr(
              "y",
              20 +
                event.y -
                dragStartY1 +
                Number(d3.select(this).attr("startY"))
            );
        } else {
          if (event.x - dragStartX1 > 0) {
            d3.select(this).attr(
              "width",
              Number(d3.select(this).attr("width")) + (event.x - thi.prevX1)
            );
          } else {
            d3.select(this).attr(
              "width",
              Number(d3.select(this).attr("width")) + (event.x - thi.prevX1)
            );
            // d3.select(this).attr("x", Number(d3.select(this).attr("x"))+event.x - dragStartX)
          }
          if (event.y - dragStartY1 < 0) {
            d3.select(this).attr(
              "height",
              Number(d3.select(this).attr("height")) + (event.y - thi.prevY1)
            );
          } else {
            d3.select(this).attr(
              "height",
              Number(d3.select(this).attr("height")) + (event.y - thi.prevY1)
            );
            // d3.select(this).attr("y", Number(d3.select(this).attr("y"))+event.y - dragStartY)
          }
          thi.prevX1 = event.x;
          thi.prevY1 = event.y;
        }
      }
      function dragEnd(event) {
        console.log("dragEnd");
        d3.select(this).attr("startX", d3.select(this).attr("x"));
        d3.select(this).attr("startY", d3.select(this).attr("y"));
      }
      let colors = this.colors;
      svg
        .append("rect")
        .attr("x", 100)
        .attr("y", 100)
        .attr("width", 100)
        .attr("height", 100)
        // .attr('fill', 'red')
        .attr("fill", colors(rectCounts))
        .attr("stroke", colors(rectCounts))
        .attr("rx", "10") // half of the previous radius value to make it more rounded
        .attr("ry", "10")
        .attr("id", "rect" + this.boxCount)
        .attr("class", "layoutRect")
        .attr("name", name)
        .attr("rect_id", this.boxCount)
        .attr("stroke-width", "2")
        .attr("fill-opacity", 0.2)
        .on("dblclick", function () {
          if (thi.scaleState1 == 0) {
            d3.select(this).attr("stroke-width", 6);
            thi.scaleState1 = 1;
          } else {
            d3.select(this).attr("stroke-width", 2);
            thi.scaleState1 = 0;
          }
        })
        .call(this.dragF1);
      svg
        .append("text")
        .attr("x", 100 + 10)
        .attr("y", 100 + 20)
        .attr("id", "rectText" + this.boxCount)
        .attr("text_id", this.boxCount)
        .attr("font-size", "14")
        // .attr("fill", "black")
        .attr("fill", colors(rectCounts))
        .style("font-family", "Montserrat-Bold, serif")
        // .style("font-size", "12px") // adjust as needed
        .text(name);
      this.boxCount = this.boxCount + 1;
    },
    zoom() {
      //定义缩放函数
      function zoomed(event) {
        d3.select(".gWapper").attr("transform", event.transform);
      }
      return d3
        .zoom()
        .scaleExtent([1 / 10, 10]) //用于设置最小和最大的缩放比例
        .on("zoom", zoomed);
    },
    // create() {
    //   this.colors = d3.scaleOrdinal(d3.schemeCategory10);
    // },
    // mounted(){
    //   Event.$on('new_box', name=>{
    //     console.log("new_box")
    //     console.log(name)
    //   })
    // },
  },
};
</script>

<style>
.svg-button-1 {
  width: 50px;
  height: 50px;
  outline: none;
  border: 0 solid;
  border-radius: 25px;
  background: none;
  margin-left: 0 !important;
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
