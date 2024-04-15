<template>
  <div style="height: 100%">
    <!--    buttons-->
    <div
      style="
        position: absolute;
        top: 27%;
        left: 0;
        width: 50px;
        background: none;
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
        <button class="svg-button" @click="open()">
          <svg
            id="arrow"
            transform="translate(4.1 0)"
            viewBox="0 0 41.72 32.14"
          >
            <path
              class="cls-1"
              d="M22.72,22.72l-6.65-6.65L0,0v32.14l9.41-9.42h13.31Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->

        <!--              <el-row>-->
        <button class="svg-button" @click="realAddNode(graphData)">
          <svg id="add" viewBox="0 0 44.72 32.14">
            <path
              class="cls-3"
              d="M15.69,0c8.67,0,15.69,7.02,15.69,15.69s-7.02,15.69-15.69,15.69S0,24.36,0,15.69,7.02,0,15.69,0Zm0,8.63c-.65,0-1.18.53-1.18,1.18v4.71h-4.71c-.65,0-1.18.53-1.18,1.18s.53,1.18,1.18,1.18h4.71v4.71c0,.65.53,1.18,1.18,1.18s1.18-.53,1.18-1.18v-4.71h4.71c.65,0,1.18-.53,1.18-1.18s-.53-1.18-1.18-1.18h-4.71v-4.71c0-.65-.53-1.18-1.18-1.18Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->

        <!--              <el-row>-->
        <button class="svg-button" @click="drawForce(graphData)">
          <svg id="reduce" viewBox="0 0 44.72 32.14">
            <path
              class="cls-1"
              d="M15.76,31.51c8.7,0,15.76-7.05,15.76-15.76S24.46,0,15.76,0,0,7.05,0,15.76s7.05,15.76,15.76,15.76h0Zm-5.91-16.94h11.82c.65,0,1.18.53,1.18,1.18s-.53,1.18-1.18,1.18h-11.82c-.65,0-1.18-.53-1.18-1.18s.53-1.18,1.18-1.18Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->

        <!--              <el-row>-->
        <button class="svg-button" @click="setupGraph">
          <svg id="reduce" viewBox="0 0 44.72 32.14">
            <path
              class="cls-1"
              d="m0,15.7c0,8.67,7.03,15.7,15.7,15.7s15.7-7.03,15.7-15.7h0C31.39,7.03,24.37,0,15.7,0,7.03,0,0,7.03,0,15.7h0Z"
            />
            <path
              class="cls-2"
              d="m15.7,10.31v-3.59l-4.49,4.49,4.49,4.49v-3.59c2.98,0,5.38,2.41,5.38,5.38s-2.41,5.38-5.38,5.38-5.38-2.41-5.38-5.38h-1.79c0,3.97,3.21,7.18,7.18,7.18s7.18-3.21,7.18-7.18c0-3.97-3.22-7.18-7.18-7.18Z"
            />
          </svg>
        </button>
        <!--              </el-row>-->
      </div>
    </div>

    <!--    Graph -->
    <div
      class="view"
      id="graph_real"
      style="
        background: #ffffff;
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        float: right;
        position: absolute;
        top: 5%;
        right: 3px;
        width: calc(100% - 50px);
        overflow: visible;
        box-shadow: 10px 4px 16px rgba(0, 0, 0, 0.3);
      "
    >
      <div style="float: left; margin-left: -80px">
        <div
          style="
            height: 30px;
            font-family: Montserrat-Bold, serif;
            font-size: 20px;
            font-weight: 600;
            color: rgb(97 108 24);
            margin-left: 95px;
            margin-top: 13px;
            text-align: start;
          "
        >
          Graph
        </div>
        <br />

        <!--  main  graph-->
        <div
          style="
            background: #ffffff;
            height: 36vh;
            width: 520px;
            border-bottom-left-radius: 18px;
            display: inline-block;
            margin-left: 2px;
            position: absolute;
            box-shadow: 10px 4px 3px rgba(0, 0, 0, 0.3);
          "
        >
          <div id="select-gallery" style="visibility: hidden">
            <!--          <div>-->
            <!--            <el-input v-model="name" placeholder="Enter your name"></el-input>-->
            <!--            <el-input v-model="targetName" placeholder="Enter target name"></el-input>-->
            <!--          </div>-->id="graph_real"
            <!--  <el-checkbox-group v-model="nodesData" >-->
            <div
              v-for="(node, index) in nodesData"
              style="display: inline-block"
            >
              <!--           <el-checkbox-button size="small" style="height:30px">{{node.name}}</el-checkbox-button>-->
              <!--            <circle r="20px" :style="'fill: '+this.colors[index]"></circle>-->
              <div
                :id="'node_span' + index"
                :style="{
                  backgroundColor: colors(index),
                  display: 'inline-block',
                  marginLeft: '8px',
                  opacity: 0.5,
                  fontSize: '7px',
                  borderRadius: '2px',
                }"
              >
                <span style="opacity: 1">{{ node.name }}</span>
              </div>
              <el-input
                style="width: 60px; margin-left: 1px"
                :id="'rel' + index"
                v-model="relInput[index]"
                size="small"
                placeholder="Relation"
              ></el-input>
            </div>
            <el-select
              v-model="addType"
              placeholder="Select Add"
              style="display: none"
            >
              <el-option
                v-for="item in addOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
            <!--  </el-checkbox-group>-->
            <!--          <br>-->
            <!--          <el-button @click="addNewNode">Add New Node</el-button>-->
            <el-button @click="realAddNode(graphData)" style="margin-left: 8px"
              >{{ "Add " + addType }}
            </el-button>
          </div>
          <!--          <svg-->
          <!--            ref="sceneGraph"-->
          <!--            style="width: 100%; height: 100%; float: left; overflow: visible"-->
          <!--          ></svg>-->
          <div
            ref="sceneGraph"
            id="mynetwork"
            style="width: 100%; height: 400px; overflow: visible"
          >
            123
          </div>
        </div>
        <div
          id="graph-gallery"
          style="
            display: inline-block;
            position: absolute;
            height: 36vh;
            width: 220px;
            margin-left: 500px;
            background: #ffffff;
            border-bottom-right-radius: 18px;
            box-shadow: 10px 4px 6px rgba(0, 0, 0, 0.3);
          "
        >
          <!--         <h1>hello</h1>-->
          <div
            style="
              height: 30px;
              font-family: Montserrat-Bold, serif;
              font-size: 16px;
              font-weight: 600;
              color: rgb(97 108 24);
              margin-top: 13px;
              text-align: center;
            "
          >
            Plants
          </div>

          <div class="img_row" v-for="(duo, index) in img_list">
            <img
              class="graph_img"
              :graph_id="2 * index"
              :src="'./src/assets/addOptions/' + img_list[index][0] + '.png'"
              width="75"
              height="75"
              :plant="img_list[index][0]"
              style="border-radius: 10px"
              v-on:dblclick="addClick"
            />
            <img
              class="graph_img"
              :graph_id="2 * index + 1"
              :src="'./src/assets/addOptions/' + img_list[index][1] + '.png'"
              width="75"
              height="75"
              :plant="img_list[index][1]"
              style="margin-left: 12px; border-radius: 10px"
              v-on:dblclick="addClick"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { defineComponent, onMounted, ref } from "vue";
import { DataSet, Network } from "vis";

export default {
  data() {
    return {
      name: "",
      targetName: "",
      nodesData1: [],
      nodesData: [],
      nodesAddCon: [],
      addType: "",
      addOptions: [
        { value: "Daisy", label: "Daisy" },
        { value: "Weeping_Willow", label: "Weeping_Willow" },
        { value: "Dogwood", label: "Dogwood" },
        { value: "Japanese_Pine", label: "Japanese_Pine" },
        { value: "Crape_Myrtle", label: "Crape_Myrtle" },
        { value: "Africanlily", label: "Africanlily" },
        { value: "bougainvillea", label: "bougainvillea" },
        { value: "Maple", label: "Maple" },
        //{value: "Yellow_Iris", label: "Yellow_Iris"},
        { value: "Blue_Jacaranda", label: "Blue_Jacaranda" },
        //{value: "Red_Tulip", label: "Red_Tulip"}],
        { value: "white_tulip", label: "white_tulip" },
      ],
      isAdd: 0,
      linksData: [],
      relInput: ["", "", "", "", "", "", "", "", "", "", "", ""],
      colors: null,
      img_list: [
        ["Africanlily", "bougainvillea"],
        ["Crape_Myrtle", "Daisy"],
        ["Dogwood", "Japanese_Pine"],
        ["Maple", "white_tulip"],
        ["Weeping_Willow", "Blue_Jacaranda"],
      ],
      networkInstance: null,
      scene_graph_data: {
        objects: ["bougainvillea", "poinciane", "dogwood", "bush", "alumroot"],
        relationships: [
          [0, "is", 1],
          [1, "is", 3],
          [0, "is", 3],
          [2, "is", 0],
          [4, "is", 2],
        ],
      },
    };
  },
  watch: {
    graphData: function (val) {
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
    graphData: Object,
  },
  mounted() {
    this.sceneGraph = this.$refs.sceneGraph;
    this.setupGraph();
  },
  methods: {
    getRandomColor() {
      const letters = "0123456789ABCDEF";
      let color = "#";
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    setupGraph() {
      const colorScale = d3.scaleOrdinal(d3.schemeCategory10); // 使用 D3 的预设颜色方案

      const nodes = new DataSet(
        this.scene_graph_data.objects.map((obj, index) => ({
          id: index,
          label: obj,
          color: { background: colorScale(index) }, // 根据索引生成颜色
        }))
      );

      const edges = new DataSet(
        this.scene_graph_data.relationships.map((rel, index) => ({
          id: `e${index + 1}`,
          from: rel[0],
          to: rel[2],
          label: rel[1],
        }))
      );

      const options = {
        autoResize: true,
        locale: "cn",
        edges: {
          arrows: { to: { enabled: true, scaleFactor: 1 } },
        },
        physics: {
          enabled: true,
        },
      };

      if (this.sceneGraph) {
        new Network(this.sceneGraph, { nodes, edges }, options);
      }
    },
    drawSceneGraph() {
      //       const svg = d3.select(this.$refs.sceneGraph);
      //       svg.selectAll("*").remove(); // Clear previous drawings
      //
      //       const svgNode = this.$refs.sceneGraph;
      //       const rect = svgNode.getBoundingClientRect();
      //       const width = rect.width;
      //       const height = rect.height;
      //
      //       const centerX = width / 2;
      //       const centerY = height / 2;
      //       const radius = Math.min(width, height) * 0.4; // 40% of the smaller dimension
      //
      // // Calculate positions for each node based on a circular layout
      //       const nodes = this.objs.map((name, idx) => {
      //         const angle = (idx / this.objs.length) * 2 * Math.PI;
      //         return {
      //           name: name,
      //           x: centerX + radius * Math.cos(angle),
      //           y: centerY + radius * Math.sin(angle)
      //         };
      //       });
      //
      // // Draw links
      //       svg.append("g")
      //           .selectAll("line")
      //           .data(this.triples)
      //           .enter().append("line")
      //           .attr("x1", d => nodes[d.source].x)
      //           .attr("y1", d => nodes[d.source].y)
      //           .attr("x2", d => nodes[d.target].x)
      //           .attr("y2", d => nodes[d.target].y)
      //           .attr("stroke", "black");
      //
      // // Draw nodes
      //       svg.append("g")
      //           .selectAll("circle")
      //           .data(nodes)
      //           .enter().append("circle")
      //           .attr("r", 20)
      //           .attr("cx", d => d.x)
      //           .attr("cy", d => d.y)
      //           .attr("fill", () => `hsl(${Math.random() * 60}, 100%, 50%)`); // random warm color
      //
      // // Add labels for the nodes
      //       svg.append("g")
      //           .selectAll("text")
      //           .data(nodes)
      //           .enter().append("text")
      //           .attr("x", d => d.x)
      //           .attr("y", d => d.y)
      //           .attr("text-anchor", "middle")
      //           .attr("dominant-baseline", "middle")
      //           .text(d => d.name);
      //
      // // Simple arrowheads
      //       svg.append("g")
      //           .selectAll("path")
      //           .data(this.triples)
      //           .enter().append("path")
      //           .attr("d", d => {
      //             const dx = nodes[d.target].x - nodes[d.source].x;
      //             const dy = nodes[d.target].y - nodes[d.source].y;
      //             const dr = Math.sqrt(dx * dx + dy * dy);
      //             const offsetX = (dx * 20) / dr;
      //             const offsetY = (dy * 20) / dr;
      //             const x = nodes[d.target].x - offsetX;
      //             const y = nodes[d.target].y - offsetY;
      //             return `M${x - 8},${y - 8}L${x},${y}L${x + 8},${y + 8}`;
      //           });
      const svg = d3.select(this.$refs.sceneGraph);
      svg.selectAll("*").remove(); // Clear previous drawings

      const svgNode = this.$refs.sceneGraph;
      const rect = svgNode.getBoundingClientRect();
      const width = rect.width;
      const height = rect.height;

      const centerX = width / 2;
      const centerY = height / 2;
      const radius = Math.min(width, height) * 0.35; // 30% of the smaller dimension
      const nodeRadius = 47; // Increased node size

      // Calculate positions for each node based on a circular layout
      const nodes = this.objs.map((name, idx) => {
        const angle = (idx / this.objs.length) * 2 * Math.PI;
        return {
          name: name,
          x: centerX + radius * Math.cos(angle),
          y: centerY + radius * Math.sin(angle),
        };
      });

      // Draw links
      svg
        .append("g")
        .attr("class", "svg_line")
        .selectAll("line")
        .data(this.triples)
        .enter()
        .append("line")
        .attr("x1", (d) => nodes[d.source].x)
        .attr("y1", (d) => nodes[d.source].y)
        .attr("x2", (d) => {
          const dx = nodes[d.target].x - nodes[d.source].x;
          const dy = nodes[d.target].y - nodes[d.source].y;
          const len = Math.sqrt(dx * dx + dy * dy);
          return nodes[d.source].x + (dx * (len - nodeRadius)) / len;
        })
        .attr("y2", (d) => {
          const dx = nodes[d.target].x - nodes[d.source].x;
          const dy = nodes[d.target].y - nodes[d.source].y;
          const len = Math.sqrt(dx * dx + dy * dy);
          return nodes[d.source].y + (dy * (len - nodeRadius)) / len;
        })
        .attr("stroke", "black");

      // Draw nodes
      svg
        .append("g")
        .attr("class", "svg_circle")
        .selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("r", nodeRadius)
        .attr("cx", (d) => d.x)
        .attr("cy", (d) => d.y)
        .attr(
          "fill",
          () =>
            `hsl(${20 + Math.random() * 40}, ${Math.random() * 20 + 70}%, ${
              Math.random() * 10 + 60
            }%)`
        ); // random warm color

      // Add labels for the nodes
      svg
        .append("g")
        .attr("class", "svg_text")
        .selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .attr("x", (d) => d.x)
        .attr("y", (d) => d.y)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .text((d) => d.name);

      // Simple arrowheads
      svg
        .append("g")
        .attr("class", "svg_path")
        .selectAll("path")
        .data(this.triples)
        .enter()
        .append("path")
        .attr("d", (d) => {
          // Total difference in x and y from source to target
          const dx = nodes[d.target].x - nodes[d.source].x;
          const dy = nodes[d.target].y - nodes[d.source].y;

          // Length of path from center of source node to center of target node
          const len = Math.sqrt(dx * dx + dy * dy);

          // x and y distances from center to outside edge of target node
          // const x = nodes[d.source].x + (dx * (len - nodeRadius) / len);
          // const y = nodes[d.source].y + (dy * (len - nodeRadius) / len);

          const x = (dx * nodes[d.target].radius) / len;
          const y = (dy * nodes[d.target].radius) / len;

          // return `M${x - 8},${y - 8}L${x},${y}L${x + 8},${y + 8}`;
          return `M${x - 8},${y - 8}L${x},${y}L${x + 8},${y + 8}`;
        });
    },
    // drawBoxes() {
    //   const svg = d3.select(this.$refs.sceneGraph);
    //   svg.selectAll("*").remove();  // Clear previous drawings
    //
    //   this.objs.forEach((obj, index) => {
    //     svg.append("rect")
    //         .attr("x", index * 150 + 10)
    //         .attr("y", 50)
    //         .attr("width", 100)
    //         .attr("height", 50)
    //         .attr("fill", "none")
    //         .attr("stroke", "black");
    //
    //     svg.append("text")
    //         .attr("x", index * 150 + 60)
    //         .attr("y", 75)
    //         .attr("text-anchor", "middle")
    //         .text(obj);
    //   });
    // }
    imgDown(event) {
      console.log(event.target.attributes.plant.value);
      // this.addType=event.target.attributes.plant.value
      // this.realAddNode(this.graphData)
      //d3.select("#graph_real").append("img").attr("class", "drag_img").style("left",event.clientX+50+"px").style("top",event.clientY+50+"px").attr("src","./src/assets/addOptions/"+event.target.attributes.plant.value+".png").attr("width","80px").attr("height","80px")
    },
    addClick(event) {
      console.log(event.target.attributes.plant.value);
      d3.select("#select-gallery").style("visibility", "visible");
      this.addType = event.target.attributes.plant.value;
      // this.realAddNode(this.graphData)

      for (let i = 0; i < this.nodesData.length; i++) {
        console.log("colors");
        console.log(this.colors(i));
        d3.select("#node_span" + i).style("background-color", this.colors(i));
      }
      event.target.style.border = "2px solid red";
    },
    // setup() {
    //   const chartRef = ref(null);
    //   let network;
    //   const scene_graph_data = {
    //     objects: ["bougainvillea", "poinciane", "dogwood", "bush", "alumroot"],
    //     relationships: [
    //       [0, "is", 1],
    //       [1, "is", 3],
    //       [0, "is", 3],
    //       [2, "is", 0],
    //       [4, "is", 2],
    //     ],
    //   };
    //
    //   // 生成节点数据
    //   const nodes = new DataSet(
    //     scene_graph_data.objects.map((obj, index) => ({
    //       id: index,
    //       label: obj,
    //       color: { background: getRandomColor() }, // 随机颜色函数
    //     }))
    //   );
    //
    //   // 生成边数据
    //   const edges = new DataSet(
    //     scene_graph_data.relationships.map((rel, index) => ({
    //       id: `e${index + 1}`,
    //       from: rel[0],
    //       to: rel[2],
    //       label: rel[1],
    //     }))
    //   );
    //
    //   // 随机颜色生成函数
    //   function getRandomColor() {
    //     const letters = "0123456789ABCDEF";
    //     let color = "#";
    //     for (let i = 0; i < 6; i++) {
    //       color += letters[Math.floor(Math.random() * 16)];
    //     }
    //     return color;
    //   }
    //
    //   // const nodes = new DataSet([
    //   //   { id: 0, label: "大前端", color: { background: "#fd91b7" } },
    //   //   { id: 1, label: "HTML", color: { background: "#7ed6df" } },
    //   //   { id: 2, label: "JavaScript", color: { background: "#d294e2" } },
    //   //   { id: 3, label: "CSS", color: { background: "#ffb300" } },
    //   // ]);
    //   //
    //   // const edges = new DataSet([
    //   //   { id: "e1", from: 0, to: 1, label: "含" },
    //   //   { id: "e2", from: 1, to: 0, label: "嵌" },
    //   //   { id: "e3", from: 0, to: 2, label: "step1" },
    //   //   { id: "e4", from: 0, to: 3, label: "step1" },
    //   // ]);
    //
    //   const options = {
    //     autoResize: true,
    //     locale: "cn",
    //     locales: {
    //       cn: {
    //         edit: "编辑",
    //         del: "删除当前节点或关系",
    //         back: "返回",
    //         addNode: "添加节点",
    //         addEdge: "添加连线",
    //         editNode: "编辑节点",
    //         editEdge: "编辑连线",
    //         addDescription: "点击空白处可添加节点",
    //         edgeDescription: "点击某个节点拖拽连线可连接另一个节点",
    //         editEdgeDescription: "可拖拽连线改变关系",
    //         createEdgeError: "无法将边连接到集群",
    //         deleteClusterError: "无法删除集群.",
    //         editClusterError: "无法编辑群集'",
    //       },
    //     },
    //     nodes: {
    //       shape: "dot",
    //       size: 30,
    //       shadow: false,
    //       font: {
    //         size: 18,
    //         color: "rgb(117, 218, 167)",
    //         align: "center",
    //       },
    //       color: {
    //         border: "transparent",
    //         background: "#ffc7c7",
    //         highlight: {
    //           border: "rgb(255, 0, 0)",
    //           background: "rgb(255, 0, 0)",
    //         },
    //         hover: {
    //           border: "#dff9fb",
    //           background: "#88dab1",
    //         },
    //       },
    //       margin: 5,
    //       widthConstraint: 100,
    //       borderWidth: 1,
    //       borderWidthSelected: 3,
    //       labelHighlightBold: false,
    //     },
    //     edges: {
    //       width: 1,
    //       length: 200,
    //       color: {
    //         color: "#848499",
    //         highlight: "rgb(255, 85, 0)",
    //         hover: "#88dab1",
    //         inherit: "from",
    //         opacity: 1.0,
    //       },
    //       arrows: { to: true },
    //     },
    //     physics: {
    //       enabled: true,
    //       barnesHut: {
    //         gravitationalConstant: -4000,
    //         centralGravity: 0.3,
    //         springLength: 120,
    //         springConstant: 0.04,
    //         damping: 0.09,
    //         avoidOverlap: 0,
    //       },
    //     },
    //   };
    //   onMounted(() => {
    //     if (chartRef.value) {
    //       network = new Network(chartRef.value, { nodes, edges }, options);
    //     }
    //   });
    //   return { chartRef };
    // },
    drawForce(scene_graph_data) {
      // scene_graph_data = {
      //   objects: ["bougainvillea", "poinciane", "dogwood", "bush", "alumroot"],
      //   relationships: [
      //     [0, "is", 1],
      //     [1, "is", 3],
      //     [0, "is", 3],
      //     [2, "is", 0],
      //     [4, "is", 2],
      //   ],
      // };
      let sceneGraph = scene_graph_data;
      console.log(scene_graph_data["objects"]);
      //数据
      // let nodesData = [{name: "桂林", id: 0}, {name: "广州", id: 1},
      //   {name: "厦门", id: 2}, {name: "杭州", id: 3},
      //   {name: "上海", id: 4}, {name: "青岛", id: 5},
      //   {name: "天津", id: 6}];
      // this.nodesData = nodesData;
      //
      // let linksData = [{source: 0, target: 1}, {source: 0, target: 2},
      //   {source: 0, target: 3}, {source: 1, target: 4},
      //   {source: 1, target: 5}, {source: 1, target: 6}];
      // this.linksData = linksData;

      // Transform objects to nodesData
      let nodesData;
      if (this.isAdd == 0) {
        nodesData = sceneGraph.objects.map((name, index) => ({
          name: name, // Object name
          id: index, // Index of the object in the array, acting as the ID
        }));
        this.nodesData = nodesData;
        console.log(nodesData);
      } else {
        nodesData = this.nodesData;
      }

      this.nodesAddCon = [];
      for (let i = 0; i < this.nodesData.length; i++) {
        this.nodesAddCon.push("");
      }
      console.log(this.nodesAddCon);

      // Transform relationships to linksData
      let linksData;
      if (this.isAdd == 0) {
        linksData = sceneGraph.relationships.map((relationship) => ({
          source: relationship[0], // First element of the relationship array
          relationship: relationship[1], // Second element of the relationship array
          target: relationship[2], // Third element of the relationship array
        }));
        this.linksData = linksData;
      } else {
        linksData = this.linksData;
      }

      console.log(linksData);

      //开始布局画图
      const svg = d3.select(this.$refs.sceneGraph);
      svg.selectAll("*").remove(); // Clear previous drawings

      const svgNode = this.$refs.sceneGraph;
      const rect = svgNode.getBoundingClientRect();
      const width = rect.width;
      const height = rect.height;

      //初始化力学仿真器
      let simulation = d3
        .forceSimulation(nodesData) //使用指定的nodes创建一个新的没有任何力模型的仿真
        .force(
          "link",
          d3.forceLink(linksData).id((d) => d.id)
        ) //弹簧力，为仿真添加指定name的力模型并返回仿真
        // .force('charge', d3.forceManyBody().strength(-2000))  //电荷力/万有引力/多体力
        .force("charge", d3.forceManyBody().strength(-10000))
        .force("center", d3.forceCenter(width / 2, height / 2)) //向心力
        .on("tick", this.ticked.bind(this));
      this.simulation = simulation;

      //定义一个序数颜色比例尺
      var color = d3.scaleOrdinal(d3.schemeCategory10);

      this.colors = color;

      svg
        .append("defs")
        .append("marker")
        .attr("id", "end")
        .attr("viewBox", "-0 -5 10 10")
        .attr("markerUnits", "userSpaceOnUse")
        .attr("refX", 31)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 10)
        .attr("markerHeight", 10)
        .append("svg:path")
        .attr("d", "M 0,-5 L 10 ,0 L 0,5")
        .attr("fill", "#ccc")
        .attr("stroke", "#ccc");

      // svg.selectAll("text")
      //     .data(linksData)
      //     .enter()
      //     .append("text")
      //     .style("fill", "black")
      //     .attr("x", function (d) {
      //       const source = nodeCoordinates[d[0]];
      //       const target = nodeCoordinates[d[2]];
      //       return (source.x + target.x) / 2; // x-coordinate of the midpoint
      //     })
      //     .attr("y", function (d) {
      //       const source = nodeCoordinates[d[0]];
      //       const target = nodeCoordinates[d[2]];
      //       return (source.y + target.y) / 2; // y-coordinate of the midpoint
      //     })
      //     .text(function (d) {
      //       return d[1]; // the relationship description
      //     });

      //添加group
      let gWapper = svg
        .append("g")
        .attr("class", "gWapper")
        .attr("cursor", "pointer");
      //绘制连线
      this.links = gWapper
        .append("g") //root
        .selectAll("line") //dom
        .data(linksData) //model
        .enter()
        .append("line")
        .attr("stroke", "blue")
        .attr("stroke-width", 1)
        .attr("marker-end", "url(#end)");
      // .on('mouseover', function (d, i) {
      //   d3.select(this).attr('stroke', 'red');
      //   d3.select('#linkText' + i).style('visibility', 'visible');
      //   d3.select('#linkRect' + i).style('visibility', 'visible');
      // })
      // .on('mouseout', function (d, i) {
      //   d3.select(this).attr('stroke', 'blue');
      //   d3.select('#linkText' + i).style('visibility', 'hidden');
      //   d3.select('#linkRect' + i).style('visibility', 'hidden');
      // })

      this.linkRects = gWapper
        .append("g") //root
        .selectAll("line") //dom
        .data(linksData) //model
        .enter()
        .append("rect")
        .attr("class", "textRect")
        .attr("id", (d, i) => "linkRect" + i)
        .style("fill", "white")
        .style("stroke", "black")
        // .style('visibility', 'hidden')
        // .attr("stroke", "blue")
        .attr("stroke-width", 1);
      // .attr("marker-end", 'url(#end)');

      // let textnode = gWapper.append('g')
      //     .selectAll('text')
      //     .data(linksData)
      //     .enter()
      //     .append('text')
      //     .style("fill", "black")
      //     .attr("x", textnode => {
      //       const link = linksData.find(link => link.source.id === d[0] && link.target.id === d[2]);
      //       if (link) {
      //         return (link.source.x + link.target.x) / 2;
      //       }
      //     })
      //     .attr("y", function (d) {
      //       const link = linksData.find(link => link.source.id === d[0] && link.target.id === d[2]);
      //       if (link) {
      //         return (link.source.y + link.target.y) / 2;
      //       }
      //     })
      //     .text(function (d) {
      //       return d[1]; // the relationship description
      //     });
      // this.textnode = textnode;

      //绘制箭头
      //  let arrow = gWapper.append('defs')
      //     .append('marker')
      //     .attr('id', 'arrow')
      //     .attr('markerWidth', 20)
      //     .attr('markerHeight', 20)
      //     .attr('refX', 8)
      //     .attr('refY', 8)
      //     .attr('orient', 'auto')
      //     .append('path')
      //     .attr('fill', 'red')
      //     .attr('d', 'M0 0 L8 8 L0 16Z')

      //绘制节点
      this.nodes = gWapper
        .append("g")
        .selectAll("circle")
        .data(nodesData)
        .enter()
        .append("circle")
        .attr("r", 25)
        .attr("opacity", 0.5)
        .attr("fill", (d, i) => {
          return color(i);
        })
        .call(this.drag);

      //取消默认右击菜单，自定义菜单
      // .on('contextmenu ', (event, d) => {
      //   event.preventDefault()
      //   this.isShowTip = true;
      //   this.point = {
      //     left: event.offsetX,
      //     top: event.offsetY,
      //     data: d
      //   }
      // });

      //绘制文字
      let texts = gWapper
        .append("g")
        .selectAll("text")
        .data(nodesData)
        .enter()
        .append("text")
        .attr("font-size", "12px")
        .attr("text-anchor", "middle")
        .attr("dy", "0.3em")
        .text((d) => d.name)
        .call(this.drag);
      let linkTexts = gWapper
        .append("g")
        .selectAll(".linktext")
        .data(linksData)
        .enter()
        .append("text")
        .attr("font-size", "12px")
        .attr("class", "linktext")
        .attr("text-anchor", "middle")
        .attr("dy", "0.3em")
        .attr("id", (d, i) => "linkText" + i)
        // .style('visibility', 'hidden')
        .text((d) => d.relationship)
        .call(this.drag);

      this.texts = texts;
      this.linkTexts = linkTexts;
    },
    realAddNode(graphData) {
      this.isAdd = 1;
      for (let i = 0; i < this.nodesData.length; i++) {
        console.log(this.relInput[i]);
        if (this.relInput[i] != "") {
          let newLinks = [
            {
              source: i,
              target: this.nodesData.length,
              relationship: this.relInput[i],
            },
          ];
          this.linksData.push(newLinks[0]);
        }
      }
      this.nodesData.push({ name: this.addType, id: this.nodesData.length });
      this.drawForce(graphData);
      for (let i = 0; i < this.nodesData.length; i++) {
        this.relInput[i] = "";
      }
      // this.linksData.push
      this.isAdd = 0;
      // let svg=d3.select("#layoutBox")
      // svg.append("rect")
      // Event.$emit('new_box', this.addType);
      d3.select("#select-gallery").style("visibility", "hidden");
      d3.selectAll(".graph_img").style("border", "none");
      this.$emit("new_box", this.addType);
    },
    addNewNode() {
      const nodeName = this.name.trim();
      const targetName = this.targetName.trim();
      if (nodeName) {
        if (!this.nodesData1 || this.nodesData1.length === 0) {
          this.nodesData1 = this.nodesData1 || []; // Initialize if not already
          this.nodesData1.push({ name: nodeName, id: 100, target: targetName });
        } else {
          const lastID = this.nodesData1[this.nodesData1.length - 1].id;
          this.nodesData1.push({
            name: nodeName,
            id: lastID + 1,
            target: targetName,
          });
        }
      }
      console.log(this.nodesData1);
      this.name = ""; // Reset the input
      this.targetName = ""; // Reset the input
    },
    addNode() {
      //动态增加节点
      let newNodes = [
        { name: "河北", id: 5 },
        { name: "青岛", id: 6 },
      ];
      let newLinks = [
        { source: 5, target: 0 },
        { source: 6, target: 1 },
      ];

      let newAddFlag = false;
      for (let item of newNodes) {
        const index = this.nodesData.findIndex((d) => d.id === item.id);
        if (index === -1) {
          this.nodesData.push(item);
          newAddFlag = true;
        }
      }
      for (let item of newLinks) {
        const index = this.linksData.findIndex(
          (d) => d.source.id === item.source && d.target.id === item.target
        );
        const reverseIndex = this.linksData.findIndex((d) => {
          return d.source.id === item.target && d.target.id === item.source;
        });
        if (index === -1) {
          //新增连线
          this.linksData.push(item);
          newAddFlag = true;
        }
        if (reverseIndex > -1) {
          //新增箭头
          item.isReverse = true;
          this.linksData.push(item);
          newAddFlag = true;
        }
      }
      if (!newAddFlag) {
        console.log("未新增节点和连线");
      }
      this.update("add");
    },
    delNode() {
      let nodeIndex = this.nodesData.findIndex(
        (d) => d.id === this.point.data.id
      );
      this.nodesData.splice(nodeIndex, 1);
      this.linksData.forEach((d, i) => {
        if (
          d.source.id === this.point.data.id ||
          d.target.id === this.point.data.id
        ) {
          this.linksData.splice(i, 1);
        }
      });
      this.isShowTip = false;
      this.update("del");
    },
    update(addOrDel) {
      //定义一个序数颜色比例尺
      var color = d3.scaleOrdinal(d3.schemeCategory10);
      if (addOrDel === "add") {
        this.nodes = this.nodes
          .data(this.nodesData, (d) => d.name)
          .enter()
          .append("circle")
          .merge(this.nodes);
        this.texts = this.texts
          .data(this.nodesData, (d) => d.name)
          .enter()
          .append("text")
          .merge(this.texts);
        this.links = this.links
          .data(this.linksData, (d) => {
            return d.source.name + "-" + d.target.name;
          })
          .enter()
          .append("line")
          .attr("marker-end", "url(#end)") // Add this line to apply the arrow marker
          .attr("stroke", "blue")
          .attr("stroke-width", 1)
          .merge(this.links);
      } else if (addOrDel === "del") {
        this.nodes = this.nodes
          .data(this.nodesData, (d) => d.name)
          .exit()
          .remove("circle")
          .merge(this.nodes);
        this.texts = this.texts
          .data(this.nodesData, (d) => d.name)
          .exit()
          .remove("text")
          .merge(this.texts);
        this.links = this.links
          .data(this.linksData, (d) => {
            return d.source.name + "-" + d.target.name;
          })
          .exit()
          .remove("line")
          .merge(this.links);
      }
      this.nodes
        .attr("r", 20)
        .attr("opacity", 0.5)
        .attr("fill", (d, i) => {
          return color(i);
        })
        .call(
          d3
            .drag()
            .on("start", this.dragstart)
            .on("drag", this.dragged)
            .on("end", this.dragend)
        )
        //取消默认右击菜单，自定义菜单
        .on("contextmenu ", (event, d) => {
          event.preventDefault();
          this.isShowTip = true;
          this.point = {
            left: event.offsetX,
            top: event.offsetY,
            data: d,
          };
        });

      this.texts = this.texts
        .attr("text-anchor", "middle")
        .attr("dy", "0.3em")
        .text(function (d) {
          return d.name;
        })
        .call(
          d3
            .drag()
            .on("start", this.dragstart)
            .on("drag", this.dragged)
            .on("end", this.dragend)
        );

      this.links = this.links
        .attr("stroke", (d) => {
          return d.isReverse ? "none" : "blue";
        })
        .attr("stroke-width", 1)
        .attr("marker-end", "url(#arrow)");

      this.simulation.nodes(this.nodesData);
      this.simulation.force("link").links(this.linksData);
      this.simulation.alpha(1).restart();
    },
    ticked() {
      //虽然仿真系统会更新节点的位置(只是设置了nodes对象的x y属性)，但是它不会转为svg内部元素的坐标表示，这需要我们自己来操作
      this.links
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);
      // .attr('x', d=>(d.source.x+d.target.x)/2)
      // .attr('y', d=>(d.source.y+d.target.y)/2)

      this.nodes
        .attr("cx", (d) => {
          return d.x;
        })
        .attr("cy", (d) => d.y);

      this.texts.attr("x", (d) => d.x).attr("y", (d) => d.y);

      this.linkTexts
        // .attr('x', d => d.x)
        // .attr('y', d => d.y)
        .attr("x", (d) => (d.source.x + d.target.x) / 2)
        .attr("y", (d) => (d.source.y + d.target.y) / 2)
        // .attr('transform', function (d) {
        //   return 'rotate(' + ((Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x) * 180 / Math.PI)-180) + ',' + (d.source.x + d.target.x) / 2 + ',' + (d.source.y + d.target.y) / 2 + ')';
        // });
        .attr("transform", function (d) {
          let angle =
            (Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x) *
              180) /
            Math.PI;
          if (angle > 90) {
            angle = angle - 180;
          }
          return (
            "rotate(" +
            angle +
            "," +
            (d.source.x + d.target.x) / 2 +
            "," +
            (d.source.y + d.target.y) / 2 +
            ")"
          );
        });

      this.linkRects
        .attr(
          "x",
          (d) => (d.source.x + d.target.x) / 2 - d.relationship.length * 3
        )
        .attr("y", (d) => (d.source.y + d.target.y) / 2 - 10)
        .attr("width", (d) => d.relationship.length * 6)
        .attr("height", 20)
        .attr("transform", function (d) {
          return (
            "rotate(" +
            ((Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x) *
              180) /
              Math.PI -
              180) +
            "," +
            (d.source.x + d.target.x) / 2 +
            "," +
            (d.source.y + d.target.y) / 2 +
            ")"
          );
        });
      if (this.simulation.alpha() < 0.2) {
        this.nodes
          .attr("cx", (d) => {
            d.fx = d.x;
            return d.x;
          })
          .attr("cy", (d) => {
            d.fy = d.y;
            return d.y;
          });
        this.simulation.stop();
      }
    },
    drag(simulation) {
      function dragstart(event, d) {
        if (!event.active) {
          simulation.alphaTarget(0.3).restart();
        }
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragend(event, d) {
        if (!event.active) {
          simulation.alphaTarget(0);
        }
        d.fx = null;
        d.fy = null;
      }

      return d3
        .drag()
        .on("start", dragstart)
        .on("drag", dragged)
        .on("end", dragend);
    },
    zoom() {
      //定义缩放函数
      var zoom = d3
        .zoom()
        .scaleExtent([1 / 10, 10]) //用于设置最小和最大的缩放比例
        .on("zoom", zoomed);

      function zoomed(event) {
        d3.select(".gWapper").attr("transform", event.transform);
      }

      return zoom;
    },
    create() {
      this.colors = d3.scaleOrdinal(d3.schemeCategory10);
    },
  },
};
</script>

<style>
.svg-button {
  width: 50px;
  height: 50px;
  outline: none;
  border: 0 solid;
  border-radius: 25px;
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

line {
  stroke: #999;
  stroke-opacity: 0.6;
}

circle {
  stroke: #000;
  stroke-width: 1.5;
}
</style>
