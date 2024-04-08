<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-11-20 23:25:35
 * @LastEditTime: 2023-01-27 08:31:53
-->


<template>
 

<el-row>
<el-col :span="7">

<div id="searchPrompt" style="width:600px;height:700px;border: 5px solid;border-radius: 8px;margin-left:20px;margin-top: 25px;overflow-y: scroll;float:left">
    <div style="width:100%;height:30px;background-color: rgb(227, 245, 239);">
    <span style="font-size: large;">Search Prompts</span>
</div>
<!--    <el-form :model="formData">-->
<!--        <el-input v-model="formData.name" placeholder="search related prompt" class="input-with-select" style="width:500px">-->
<!--            <template #append>-->
<!--            <div style="width: 50px; margin-top: -10px;">-->
<!--                <el-button @click="PromptSearch()">-->
<!--                    <el-icon :size="25">-->
<!--                        <Search />-->
<!--                    </el-icon>-->
<!--                </el-button>-->
<!--            </div>-->
<!--        </template>-->
<!--        </el-input>-->
<!--    </el-form>-->
</div>

<div id="searchPrompt1" style="width:800px;height:700px;border: 5px solid;border-radius: 8px;margin-left:80px;margin-top: 85px;overflow-y: scroll;float:left">
    <span style="font-size: large;">Search Prompts</span>
</div>



<br>
<br>
<div>
<p id="currentPrompt" style="font-size:larger" @mouseup="focusText()"></p>
<div class="tooltip" id="tooltip">
    <el-button @click="closeTool()" style="float:right"> <el-icon :size="20">
                    <Close />
                </el-icon>
    </el-button>
</div>
</div>
<p></p>
<div id="TestPrompt" style="width:600px;height:300px;border: 1px solid;border-radius: 8px;margin-left:20px;margin-top: 25px;overflow-y: scroll;">
        <div style="width:100%;height:30px;background-color: rgb(227, 245, 239);">
        <span style="font-size: large;">Test Generation</span>
        </div>
    
<div id="inputPrompt">
    <el-form :model="formData1">
        <el-input v-model="formData1.name" placeholder="Please enter prompt"  type="textarea" style="width:500px" :autosize="{ minRows: 2, maxRows: 5}">
            <!-- <template #append>
            <div style="width: 50px; margin-top: -10px;">
                <el-button @click="testGen()">
                    <el-icon :size="25" style="vertical-align: middle">
                       
                    </el-icon>
                </el-button>
            </div>
        </template> -->
        </el-input>
        <el-button @click="testGen()">
            Generate <el-icon :size="20" style="vertical-align: middle">
                       
                    </el-icon>
        </el-button>
    </el-form>
</div>
<!-- <div id="conceptBox">
    <el-button @click="addConcept()">addConcept</el-button>
    <el-button @click="subConcept()">submit</el-button>
    <el-button @click="deleteAllConcept()">delete</el-button>
    <el-button @click="addContextual()">contextual</el-button>
    <el-button @click="showContext()">showContext</el-button>
    <br>
    <el-button @click="showPath()">showPath</el-button>
    <el-button @click="showLAMP()">showLAMP</el-button>
    <el-button @click="showCorrelation()">showCorr </el-button>
    <el-button @click="addCompare()">addCompare </el-button>
</div> -->
<el-button @click="addCompare()">addCompare </el-button>
<div id="inputPrompt2" style="display:none">
    <el-form :model="formData2">
        <el-input v-model="formData2.name" placeholder="Please enter prompt" type="textarea" style="width:500px" :autosize="{ minRows: 2, maxRows: 5}">
            <!-- <template #append>
            <div style="width: 50px; margin-top: -10px;">
                <el-button @click="testCompare()">
                    <el-icon :size="25" style="vertical-align: middle">
                        
                    </el-icon>
                </el-button>
            </div>
        </template> -->
        </el-input>
        <el-button @click="testCompare()">
                    <el-icon :size="20" style="vertical-align: middle">
                        ✨
                    </el-icon>
        </el-button>
    </el-form>
</div>
</div>
</el-col>

<el-col :span="10">
    <div id="TestPrompt" style="width:960px;height:1000px;border: 1px solid;border-radius: 8px;margin-left:0px;margin-top: 25px;">
    <div style="width:100%;height:30px;background-color: rgb(227, 245, 239);">
    <span style="font-size: large;">Overview</span>
</div>
<el-button @click="addConcept()">addConcept</el-button>
<el-button @click="subConcept()">submit</el-button>
<el-button @click="deleteAllConcept()">delete</el-button>
<el-button @click="addContextual()">contextual</el-button>
<el-button @click="showContext()">showContext</el-button>

<el-button @click="showPath()">showPath</el-button>
<el-button @click="showLAMP()">LAMP</el-button>
<el-button @click="showCorrelation()">Corr </el-button>
<el-button @click="BLIP()">BLIP </el-button>
<el-button @click="showBLIP()">showBLIP </el-button>

<div id="overview" style="width:960px;height:720px;">



</div>
<div id="overview_im" style="display:inline-block">
<img id="sample_image" width="200" height="200" style="visibility: hidden;">
<p id="cor_text"></p>
</div>  
<div id="conceptBox" style="width:300px;height:210px;overflow-y: scroll;overflow-x: scroll;border: 1px solid;border-radius: 6px;display:inline-block">

    
</div> 
```````````````````````````````````````````````````````````````````````````````````````````````<div id="vis_concept_box" style="width:100px;height:210px;overflow-y: scroll;border: 1px solid;border-radius: 6px;display:inline-block">```````````````````````````````````````````````````````````````````````````````````````````````
</div>
</div>
</el-col>
</el-row>


<div id="corr" style="display:inline-block">
    
</div>
<div id="cor_im" style="display:inline-block">
<img id="cor_image" width="150" height="150" style="visibility: hidden;">
</div>
<!-- <div id="chart" ></div>
<div style="display:inline-block"><img id="image" width="300" height="300"></div>
<el-button style="margin-top: 30px;" @click="drawCor()"> draw </el-button> -->

</template>
<script>
import { Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router';
import { dataService } from '@/service';
import { useDataStore } from "../stores/counter";
import { postImg, postText, postPrompt, fetchPrompt, postGenerate, postAxis, addGenerate, postContext, postPath, postLAMP, postBLIP } from '../service/module/dataService'
var global_control_ids=[]
export default {
    name: 'APP',
    props: ["msgH"],
    data() {
        return {
            msg1: "Hello, main!",
            moreSearch: -1,
            formData: {
                name: '',
                region: '',
                price: '',
                rarity: '',
                collection: '',
                backgroundColor: '',
                style: '',
                type: '',
            },
            formData1: {
                name: '',

            },
            formData2: {
                name: '',

            },
            imgData: {
                accept: "image/png, image/jpeg, image/jpg"
            },
            addFeature: [],
            file: '',
            imgURL: '',
            promptResults: [],
            selected_prompt: '',
            keyWord: '',
            conceptNum: 0,
            conceptList: [],
            angles: [Math.PI/3, -Math.PI/3, Math.PI, 2*Math.PI*Math.random(), 2*Math.PI*Math.random()],
            colors: ["red","blue", "yellow"],
            total_number: 50,
            sample_len: 50,
            control_ids: [],
            dragF: null,
            dragStartX: null,
            dragStartY: null,
        }
    },

    methods: {
        async drawOverview(){
            let data1 = await d3.csv("./src/assets/testSample1.csv");
            let width = 700;
            let height = 700;
            let colors=this.colors
            d3.select("#overviewSvg").remove()
            let svg = d3.select("#overview").append("svg")
            .attr("id","overviewSvg")
            .attr("width", width)
            .attr("height", height)
            .append("g").attr("id","overviewGr")
            .attr("transform", "translate(" + 100 + "," + 100 + ")");

            svg.selectAll(".node")
                .data(data1)
                .enter().append("circle")
                .attr("class","node")
                .attr("id",function(d,i){return "node"+i})
                .attr("cx",function(d,i){return 500*d["x"]})
                .attr("cy",function(d,i){return 500*d["y"]})
                .attr("r",3)
                .attr("point_id",function(d,i){return i})
                .attr("path",function(d,i){return d["path"]})
                .style("fill",function(d,i){return colors[d["id"]]})
                .on("mouseenter", function(d,i){
                    d3.select(this).attr("r",10).attr("stroke","black")
                    d3.select("#sample_image").attr("src", "./src/assets/testGen/"+d3.select(this).attr("path")).style("visibility","visible")
                })
                .on("mouseout", function(d,i){
                    d3.select(this).attr("r",3).attr("stroke","none")
                })
        },
        addContextual(){
            let formData = new FormData();
            for (let i=0; i<this.conceptNum;i++){
                console.log(document.getElementById("concept"+i).value)
                formData.append("concept"+i, document.getElementById("concept"+i).value);
                formData.append("type"+i, d3.select("#conceptBox").attr("conceptType"))
                if (d3.select("#concept"+i+"Type").attr("conceptType")=="double")
                {
                    formData.append("concept"+i+"double", document.getElementById("concept"+i+"double").value);
                }
            }
            formData.append("num",this.conceptNum);
            postContext(formData, res => {
                    console.log(res);

                });
        },
        showPath(){
            let formData = new FormData();
            for (let i=0; i<this.conceptNum;i++){
                console.log(document.getElementById("concept"+i).value)
                formData.append("concept"+i, document.getElementById("concept"+i).value);
                formData.append("type"+i, d3.select("#conceptBox").attr("conceptType"))
                if (d3.select("#concept"+i+"Type").attr("conceptType")=="double")
                {
                    formData.append("concept"+i+"double", document.getElementById("concept"+i+"double").value);
                }
            }
            formData.append("num",this.conceptNum);
            postPath(formData, res => {
                    console.log(res);
                    let id_str=res["path_str"]
                    let path_len=Number(res["path_len"])
                    let id_list=id_str.split(",")
                    let idx_list=[]
                    for (let k=0;k<id_list.length;k++){
                        if (id_list[k]!="")
                        idx_list.push(id_list[k])
                    }
                    this.control_ids=idx_list
                    global_control_ids=idx_list
                    console.log(idx_list)
                    let svg = d3.select("#overviewGr")
                    // for (let j=0;j<path_len;j++){
                        
                    // }
                    svg.selectAll(".path_link")
                    .data(idx_list)
                    .enter().append("line")
                    .attr("class","path_link")
                    .attr("x1", function(d,i){
                        // console.svg.select("#node"+idx_list[i]).attr("cx")
                        return svg.select("#node"+idx_list[i]).attr("cx")
                    })
                    .attr("y1", function(d,i){
                        return svg.select("#node"+idx_list[i]).attr("cy")
                    })
                    .attr("x2", function(d,i){
                        if (i<path_len-1)
                        {
                            return svg.select("#node"+idx_list[i+1]).attr("cx")
                        }
                        else
                        {
                            return svg.select("#node"+idx_list[i]).attr("cx")
                        }
                    })
                    .attr("y2", function(d,i){
                        if (i<path_len-1)
                        {
                            return svg.select("#node"+idx_list[i+1]).attr("cy")
                        }
                        else
                        {
                            return svg.select("#node"+idx_list[i]).attr("cy")
                        }
                    })
                    .style("stroke","gray").style("stroke-width","2px")
                    
                });
            
        },
        showLAMP(){
            let formData = new FormData();
            let control_xs=""
            let control_ys=""
            let svg = d3.select("#overviewGr")
            let idx_list=this.control_ids
            for (let i=0;i<idx_list.length;i++)
            {
                let x=Number(svg.select("#node"+idx_list[i]).attr("cx"))/500
                let y=Number(svg.select("#node"+idx_list[i]).attr("cy"))/500
                control_xs=control_xs+","+x
                control_ys=control_ys+","+y
            }
            formData.append("control_xs",control_xs)
            formData.append("control_ys",control_ys)
            postLAMP(formData, res => {
                console.log(res)
                this.showContext()
                this.showPath()
            })
        },
        BLIP(){
            let formData = new FormData();
            postBLIP(formData, res => {
                console.log(res)
            })
        },
        async showBLIP(){

            let data1 = await d3.csv("./src/assets/testBlipVis.csv");
            for (let i=0;i<data1.length;i++){
                
                d3.select("#vis_concept_box").append("p").attr("id","vis_concept_can"+i).text(data1[i]["term"])
            }
        },
        async showContext(){
            let data1 = await d3.csv("./src/assets/testSampleCon.csv");
            let width = 700;
            let height = 700;
            let colors=this.colors
            let total_number=this.total_number
            d3.select("#overviewSvg").remove()
            let svg = d3.select("#overview").append("svg")
            .attr("id","overviewSvg")
            .attr("width", width)
            .attr("height", height)
            .append("g").attr("id","overviewGr")
            .attr("transform", "translate(" + 100 + "," + 100 + ")");

            this.dragF=d3.drag()
            .on('start', dragStart) // 拖动开始，触发一次
            .on('drag', draged) // 拖动中，触发多次
            .on('end', dragEnd) // 拖动结束，触发一次
            .container(d3.select("#overviewSvg"))
            function dragStart(event){
                console.log("dragStart")
                d3.select(this).attr("cx",event.x+Number(d3.select(this).attr("startX"))).attr("cy",event.y+Number(d3.select(this).attr("startY")))
            }

            let control_ids=this.control_ids

            function draged(event){
                // let {x, y}= d3.event
                let gr=d3.select("#overviewGr")
                // let mouse=d3.mouse(gr)
                // console.log("event_x")
                // console.log(event.x)
                // console.log("event_y")
                // console.log(event.y)
                d3.select(this).attr("cx",event.x+Number(d3.select(this).attr("startX"))).attr("cy",event.y+Number(d3.select(this).attr("startY")))
                let idx_list=global_control_ids
                console.log("idx_list")
                console.log(idx_list)
                if (idx_list.length>0){
                    let idx=(d3.select(this).attr("point_id")).toString()
                    if (idx_list.indexOf(idx)!=-1){
                        let svg = d3.select("#overviewGr")
                        let path_len=idx_list.length
                        // for (let j=0;j<path_len;j++){
                            
                        // }
                        svg.selectAll(".path_link").remove()

                        svg.selectAll(".path_link")
                        .data(idx_list)
                        .enter().append("line")
                        .attr("class","path_link")
                        .attr("x1", function(d,i){
                            // console.svg.select("#node"+idx_list[i]).attr("cx")
                            return svg.select("#node"+idx_list[i]).attr("cx")
                        })
                        .attr("y1", function(d,i){
                            return svg.select("#node"+idx_list[i]).attr("cy")
                        })
                        .attr("x2", function(d,i){
                            if (i<path_len-1)
                            {
                                return svg.select("#node"+idx_list[i+1]).attr("cx")
                            }
                            else
                            {
                                return svg.select("#node"+idx_list[i]).attr("cx")
                            }
                        })
                        .attr("y2", function(d,i){
                            if (i<path_len-1)
                            {
                                return svg.select("#node"+idx_list[i+1]).attr("cy")
                            }
                            else
                            {
                                return svg.select("#node"+idx_list[i]).attr("cy")
                            }
                        })
                        .style("stroke","gray").style("stroke-width","2px")
                    }
                }
            }

            function dragEnd(event){
                console.log("dragStart")
                d3.select(this).attr("startX",event.x+Number(d3.select(this).attr("startX"))).attr("startY",event.y+Number(d3.select(this).attr("startY")))
            }

            svg.selectAll(".node")
                .data(data1)
                .enter().append("circle")
                .attr("class","node")
                .attr("id",function(d,i){return "node"+i})
                .attr("cx",function(d,i){return 500*d["x"]})
                .attr("cy",function(d,i){return 500*d["y"]})
                .attr("startX",function(d,i){return 500*d["x"]})
                .attr("startY",function(d,i){return 500*d["y"]})
                .attr("r",3)
                .attr("point_id",function(d,i){return i})
                .attr("path",function(d,i){return d["path"]})
                .attr("correlation", function(d, i){return d["concept1"]})
                .style("fill",function(d,i){return colors[d["id"]]})
                .on("mouseenter", function(d,i){
                    d3.select(this).attr("r",10).attr("stroke","black")
                    d3.select("#sample_image").attr("src", "./src/assets/testGen/"+d3.select(this).attr("path")).style("visibility","visible")
                    d3.select("#cor_text").text(d3.select(this).attr("correlation"))
                })
                .on("mouseout", function(d,i){
                    d3.select(this).attr("r",3).attr("stroke","none")
                })
                .call(this.dragF)
            svg.selectAll(".conlab")
                .data(data1)
                .enter().append("text")
                .attr("class","conlab")
                .attr("x",function(d,i){return 500*d["x"]})
                .attr("y",function(d,i){return 500*d["y"]})
                .text(function(d,i){
                    if (i<total_number){
                        return ''
                    }
                    else{
                        return document.getElementById("concept"+(i-total_number)).value
                    }
                })
        },
        async showCorrelation(){
            d3.select("#corrSvg").remove()
            let data2 = await d3.csv("./src/assets/testSample1.csv");
            let link = d3.linkVertical()
            .x(function(d) {
                return d.x;
            })
            .y(function(d) {
                return d.y;
            });
            let maxes=[]
            let mins=[]
            let axes=[]
            let allData=[]
            let axesLen=300;
            let width=800;
            let height=800;
            let colors=this.colors
            let Gen = d3.line() 
                .x((p) => p.x) 
                .y((p) => p.y) 
                .curve(d3.curveCatmullRom)
            let svg = d3.select("#corr").append("svg")
            .attr("id","corrSvg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + 0 + "," + 0 + ")");
            for (let i=0;i<this.conceptNum;i++){
                let data1 = await d3.csv('./src/assets/testSample_Axis'+i+'.csv');
                allData.push(data1)
                axes.push({"x":200, "y":200})
                let min0=5;
                let max0=-5;
                for (let j=0;j<data1.length;j++){
                    if (data1[j]["correlation"]<min0)
                    {
                        min0=data1[j]["correlation"];
                    }
                    if (data1[j]["correlation"]>max0)
                    {
                        max0=data1[j]["correlation"];
                    }
                }
                maxes.push(max0)
                mins.push(min0)
            }
            let allMax=-5
            let allMin=5
            for (let i=0;i<this.conceptNum;i++){
                if (maxes[i]>allMax){
                    allMax=maxes[i]
                }
                if (mins[i]<allMin){
                    allMin=mins[i]
                }
            }
            for (let i=0;i<this.total_number;i++)
            {
                let points=[]
                for (let j=0;j<this.conceptNum;j++)
                {
                    // let point= {x:100+axes[j]["x"]+((allData[j][i]["correlation"]-mins[j])/(maxes[j]-mins[j]))*axesLen*Math.cos(this.angles[j]),  y:100+axes[j]["y"]+((allData[j][i]["correlation"]-mins[j])/(maxes[j]-mins[j]))*axesLen*Math.sin(this.angles[j])}
                    // let point= {x:100+axes[j]["x"]+((allData[j][i]["correlation"]+1))*axesLen*Math.cos(this.angles[j]),  y:100+axes[j]["y"]+((allData[j][i]["correlation"]+1))*axesLen*Math.sin(this.angles[j])}
                    let point= {x:100+axes[j]["x"]+((allData[j][i]["correlation"]-mins[j])/(maxes[j]-mins[j]))*axesLen*Math.cos(this.angles[j]),  y:100+axes[j]["y"]+((allData[j][i]["correlation"]-mins[j])/(maxes[j]-mins[j]))*axesLen*Math.sin(this.angles[j])}
                    points.push(point)
                }
                console.log(points)
                console.log(Gen(points))
                svg.append("path") 
                .attr("d", Gen(points))
                .attr("class","link") 
                .attr("fill", "none") 
                // .attr("stroke", "#F4A460")
                .attr("stroke", colors[data2[i]["id"]])
                .attr("p_id", data2[i]["id"])
                .attr("path", data2[i]["path"])
                .style("stroke-width", "1px")
                .on("mouseenter", function(d){
                    d3.select(this).style("stroke", "#00BFFF").style("stroke-width", "4px")
                    d3.select("#cor_image").attr("src", "./src/assets/testGen/"+d3.select(this).attr("path")).style("visibility","visible")
                })
                .on("mouseout", function(d){
                    d3.select(this).style("stroke", colors[Number(d3.select(this).attr("p_id"))]).style("stroke-width", "1px")
                })
                ; 
            }
            let angles=this.angles
            svg.selectAll(".axes")
            .data(axes).enter()
            .append("line")
            .attr("class","axes")
            .attr("lineId",function(d,i){return i})
            .attr("x1",function(d,i){return 100+d["x"]})
            .attr("y1",function(d,i){return 100+d["y"]})
            .attr("x2",function(d,i){return 100+d["x"]+axesLen*Math.cos(angles[i])})
            .attr("y2",function(d,i){return 100+d["y"]+axesLen*Math.sin(angles[i])})
            .style("stroke","gray").style("stroke-width","2px")

            svg.selectAll(".textLabel")
            .data(axes).enter()
            .append("text").text(function(d,i){return document.getElementById("concept"+i).value})
            .attr("class","textLabel")
            .attr("x",function(d,i){return 100+d["x"]+axesLen*Math.cos(angles[i])})
            .attr("y",function(d,i){return 100+d["y"]+axesLen*Math.sin(angles[i])})

            svg.selectAll(".textLabel2")
            .data(axes).enter()
            .append("text").text(function(d,i){
                if (d3.select("#concept"+i+"Type").attr("conceptType")=="double")
                {
                    console.log("hello-concept")
                    return document.getElementById("concept"+i+"double").value
                    
                }
                else{
                    return ""
                }
            })
            .attr("class","textLabel2")
            .attr("x",function(d,i){return 100+d["x"]+0.2*axesLen*Math.cos(angles[i])})
            .attr("y",function(d,i){return 100+d["y"]+0.2*axesLen*Math.sin(angles[i])})
            
            
        },
        async drawCor(){
            let data1 = await d3.csv("./src/assets/Monet-VanGogh1.csv");
            // d3.csv("./src/assets/Monet-VanGogh1.csv", function(data1) {
                console.log("loaded")
                // let width = 1360;
                // let height = 960
                let width = 100;
                let height = 100
                let innerRadius = 40
                let outerRadius = 640
                let R=800
                let majorAngle = 2 * Math.PI / 3
                let minorAngle = 1 * Math.PI / 12;
                let angle = d3.scaleOrdinal()
            .domain(["Axis0", "Axis1"])
            .range([0, Math.PI/2]);
            let color=d3.scaleOrdinal()
            .domain(["Monet","VanGogh"])
            .range(["red","blue"])
            let radius = d3.scaleLinear()
            .range([innerRadius, outerRadius]);
            let nodes0=[]
            let nodes1=[]
            //   var nodes2=[]
            //   var nodes3=[]
            let nodes=[nodes0,nodes1]
            let edges01=[]
            for (let i=0;i<data1.length;i++)
            {
                // for (let j=0;j<2;j++)
                // {
                //     nodes[j].push(Math.random())
                // }
                nodes[0].push(data1[i]["MV"])
                nodes[1].push(data1[i]["bridge"])
            }
            for (let i=0;i<nodes[0].length;i++)
            {
                let dat=
                {
                    source: {
                        x: Math.cos(angle("Axis0")-Math.PI/2)*nodes[0][i]*R,
                        y: Math.sin(angle("Axis0")-Math.PI/2)*nodes[0][i]*R
                    },
                    target: {
                        x: Math.cos(angle("Axis1")-Math.PI/2)*nodes[1][i]*R,
                        y: Math.sin(angle("Axis1")-Math.PI/2)*nodes[1][i]*R
                    }
                };
                edges01.push(dat)

            }
            //   var edges12=[]

            //   for (let i=0;i<nodes[1].length;i++)
            //   {
            //     dat=
            //     {
            //         source: {
            //             x: Math.cos(angle("Axis1")-Math.PI/2)*nodes[1][i]*300,
            //             y: Math.sin(angle("Axis1")-Math.PI/2)*nodes[1][i]*300
            //         },
            //         target: {
            //             x: Math.cos(angle("Axis2")-Math.PI/2)*nodes[2][i]*300,
            //             y: Math.sin(angle("Axis2")-Math.PI/2)*nodes[2][i]*300
            //         }
            //     };
            //     edges12.push(dat)

            //   }

            console.log(nodes[0])
            console.log(edges01)
            let axistypes=["Axis0", "Axis1", "Axis2", "Axis3"]
            let svg = d3.select("#chart").append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + (300+outerRadius * .20) + "," + (500+outerRadius * .57) + ")");

            svg.selectAll(".axis")
                .data(axistypes)
                .enter().append("line")
                .attr("class", "axis")
                .attr("transform", function(d,i) {
                return "rotate(" + degrees(angle(axistypes[i])) + ")";
                })
                .attr("x1", 15)
                .attr("x2", function(d) {
                return 300;
                });
            svg.selectAll(".node0")
                .data(data1)
                .enter().append("circle")
                .attr("cx",function(d,i){return Math.cos(angle("Axis0")-Math.PI/2)*data1[i]["MV"]*R})
                .attr("cy",function(d,i){return Math.sin(angle("Axis0")-Math.PI/2)*data1[i]["MV"]*R})
                .attr("r",3)
                .style("fill",function(d,i){return color(data1[i]["type"])})
                .on("mouseenter", function(d,i){
                    d3.select(this).attr("r",10).attr("stroke","black")
                    d3.select("#image").attr("src", "./src/assets/"+data1[i]["path"].split("/")[2]+"/"+data1[i]["path"].split("/")[3])
                })
                .on("mouseout", function(d,i){
                    d3.select(this).attr("r",3).attr("stroke","none")
                })
            svg.selectAll(".node1")
                .data(nodes[0])
                .enter().append("circle")
                .attr("cx",function(d,i){return Math.cos(angle("Axis1")-Math.PI/2)*data1[i]["bridge"]*R})
                .attr("cy",function(d,i){return Math.sin(angle("Axis1")-Math.PI/2)*data1[i]["bridge"]*R})
                .attr("r",3)
                .style("fill",function(d,i){return color(data1[i]["type"])})
                .on("mouseenter", function(d,i){
                    d3.select(this).attr("r",10).attr("stroke","black")
                    d3.select("#image").attr("src","./src/assets/"+data1[i]["path"].split("/")[2]+"/"+data1[i]["path"].split("/")[3])
                })
                .on("mouseout", function(d,i){
                    d3.select(this).attr("r",3).attr("stroke","none")
                })
            svg.append("text")
            .attr("x",-40)
            .attr("y",-20)
            .attr("text-anchor","end")
            .text("Monet")
            .attr("font-size",25)
            svg.append("text")
            .attr("x",-40)
            .attr("y",-720)
            .attr("text-anchor","end")
            .text("Van Gogh")
            .attr("font-size",25)
            svg.append("text")
            .attr("x",480)
            .attr("y",40)
            .text("Bridge")
            .attr("font-size",25)
            // svg.selectAll(".node2")
            //     .data(nodes[0])
            //     .enter().append("circle")
            //     .attr("cx",function(d,i){return Math.cos(angle("Axis2")-Math.PI/2)*nodes[2][i]*300})
            //     .attr("cy",function(d,i){return Math.sin(angle("Axis2")-Math.PI/2)*nodes[2][i]*300})
            //     .attr("r",3)
            //     .style("fill","red")
            let link = d3.linkVertical()
            .x(function(d) {
                return d.x;
            })
            .y(function(d) {
                return d.y;
            });
            svg.append("g")
                .attr("class", "links")
                .selectAll(".link")
                .data(edges01)
                .enter().append("path")
                .attr("class", "link")
                .attr("d", function(d,i){
                    return link(edges01[i])
                })
                .attr("num_id", function(d,i){ return i})
                .attr("fill", "none")
                .style("stroke",function(d,i){
                    return color(data1[i]["type"])
                })
                // .style("stroke-opacity",0.3)
                // .style("opacity",0.1)
                // .on("mouseenter",function(d,i){
                //     d3.select(this).style("stroke-width","6px")
                //     d3.select(this).style("stroke","yellow")
                //     d3.select(this).style("stroke-opacity",1)
                //     d3.select("#image").attr("src",data1[i]["path"])
                // })
                // .on("mouseout",function(d,i){
                //     d3.select(this).style("stroke-width","1px")
                //     d3.select(this).style("stroke",color(data1[i]["type"]))
                //     d3.select(this).style("stroke-opacity",0.3)
                // })
                .style("opacity",0.3)
                .on("mouseenter",function(d){
                    // console.log(data1[0])
                    // console.log(i)
                    // console.log(d)
                    // console.log(g)
                    let num_id=Number(d3.select(this).attr("num_id"))
                    d3.select(this).style("stroke-width","6px")
                    d3.select(this).style("stroke","yellow")
                    d3.select(this).style("opacity",1)
                    d3.select("#image").attr("src","./src/assets/"+data1[num_id]["path"].split("/")[2]+"/"+data1[num_id]["path"].split("/")[3])
                })
                .on("mouseout",function(d,i){
                    d3.select(this).style("stroke-width","1px")
                    let num_id=Number(d3.select(this).attr("num_id"))
                    d3.select(this).style("stroke",color(data1[num_id]["type"]))
                    d3.select(this).style("opacity",0.3)
                })
            //   svg.append("g")
            //     .attr("class", "links")
            //     .selectAll(".link")
            //     .data(edges12)
            //     .enter().append("path")
            //     .attr("class", "link")
            //     .attr("d", function(d,i){
            //         return link(edges12[i])
            //     })
                function degrees(radians) {
            return radians / Math.PI * 180 - 90;
            }

                
            // })
        },
        PromptSearch(){
            let formData = new FormData();
            formData.append('text', this.formData.name);
            postPrompt(formData, res => {
                    console.log(res);
                    this.fetchP();
                });
            
        },
        fetchP(){
            fetchPrompt({}, res => {
                console.log(res)
                this.promptResults = res
                d3.selectAll(".pResult").remove()
                for (let i=0;i<50;i++){
                    d3.select("#searchPrompt").append("p").attr("class","pResult").text(this.promptResults[i]).on("click",this.locatePrompt)
                    .on("mouseenter", function(d,i){
                        d3.select(this).style("background-color","#E0FFFF");
                    })//.onClick(this.locatePrompt)
                    .on("mouseout", function(d,i){d3.select(this).style("background-color","white")})
                }
            });
        },
        locatePrompt(event){
            console.log("hello")
            // console.log(d3.select(this))
            console.log(event.target.innerHTML)
            d3.select("#currentPrompt").text(event.target.innerHTML)
        },
        focusText(){
            let selectedText = window.getSelection().toString();
            console.log(selectedText);
            let tool=document.getElementById("tooltip")
            tool.style.visibility="visible"
            let event = window.event||arguments[0];
	// 获取鼠标相对文本窗口的坐标 - 容器相对偏移量 = 当前需要定位的坐标
            // let y = event.pageY - event.offsetY + "px"
            // let x = event.pageX - event.offsetX + "px"
            let x = event.offsetX + "px"
            // tool.css({"top": y , "left": x});
            // tool.style.top=30
            let y= event.offsetY + 20+ "px"
            tool.style.top=y
            tool.style.left=x
            

        },
        closeTool(){
            document.getElementById("tooltip").style.visibility="hidden";
        },
        testGen(){
            let formData = new FormData();
            formData.append('text', this.formData1.name);
            postGenerate(formData, res => {
                    console.log(res);
                    this.drawOverview();
                });
        },
        addCompare(){
            document.getElementById("inputPrompt2").style.display="inline-block";

        },
        testCompare(){
            let formData = new FormData();
            formData.append('text', this.formData2.name);
            formData.append('num_id', 1);
            addGenerate(formData, res => {
                    console.log(res);
                    this.drawOverview();
                    this.total_number=this.total_number+this.sample_len
                });
        },
        addConcept(){
            d3.select("#conceptBox").append("br").attr("class","conceptBreak")
            d3.select("#conceptBox").append("div").attr("id","conceptBox"+this.conceptNum)
            d3.select("#conceptBox"+this.conceptNum).append("input").attr("class","conceptInput").attr("conceptType","single").attr("id","concept"+this.conceptNum).style("width", 100)
            // d3.select("#conceptBox").append("button").attr("class","conceptType").text("two end")
            // d3.select("#conceptBox").append("label").text("one end")
            // d3.select("#conceptBox").append("input").attr("type","radio").attr("class","conceptType").attr("name", "endType").attr("id","concept"+this.conceptNum+"single").property("checked",true)
            // d3.select("#conceptBox").append("label").text("two end")
            // d3.select("#conceptBox").append("input").attr("type","radio").attr("class","conceptType").attr("name", "endType").attr("id","concept"+this.conceptNum+"double")
            d3.select("#conceptBox"+this.conceptNum).append("select").attr("id","concept"+this.conceptNum+"Type").attr("num_id",this.conceptNum).attr("conceptType","single")
            .on("change",function(){
                // if ( d3.select("#concept"+d3.select(this).attr("num_id")+"Type").attr("value")=="single")
                if (this.value=="double")
                {
                    d3.select("#conceptBox"+d3.select(this).attr("num_id")).append("input").attr("class","conceptInput").attr("conceptType","double").attr("id","concept"+d3.select(this).attr("num_id")+"double").style("width", 100)
                    d3.select("#concept"+d3.select(this).attr("num_id")+"Type").attr("conceptType","double")
                }
                else{
                    d3.select("#concept"+d3.select(this).attr("num_id")+"double").remove()
                    d3.select("#concept"+d3.select(this).attr("num_id")+"Type").attr("conceptType","single")
                }
            })
            d3.select("#concept"+this.conceptNum+"Type").append("option").attr("value","single").text("one end")
            d3.select("#concept"+this.conceptNum+"Type").append("option").attr("value","double").text("two end")
            this.conceptNum=this.conceptNum+1
            
        },
        deleteAllConcept(){
            d3.selectAll(".conceptInput").remove();
            d3.selectAll(".conceptBreak").remove();
            this.conceptNum=0;            
        },
        subConcept(){
            let formData = new FormData();
            for (let i=0; i<this.conceptNum;i++){
                console.log(document.getElementById("concept"+i).value)
                formData.append("concept"+i, document.getElementById("concept"+i).value);
                formData.append("type"+i, d3.select("#conceptBox").attr("conceptType"))
                if (d3.select("#concept"+i+"Type").attr("conceptType")=="double")
                {
                    formData.append("concept"+i+"double", document.getElementById("concept"+i+"double").value);
                }
            }
            formData.append("num",this.conceptNum);
            postAxis(formData, res => {
                    console.log(res);
                });
        },
        translate(x, y, r) {
            return `translate(${x}, ${y}) rotate(${r})`;
        },
        jump() {
            // const router = useRouter();
            this.$router.push({ path: 'result' });
        },
        nftSearch() {
            const dataStore = useDataStore();
            // Image
            if (this.file != '' && this.formData.name == '') {
                let formData = new FormData();
                formData.append('image', this.file);
                // console.log(this.file, formData);
                postImg(formData, res => {
                    console.log(res);
                    this.jump();
                });
            }
            // Text
            else if (this.file == '' && this.formData.name != '') {
                let formData = new FormData();
                let inputText=this.formData.name
                for (let key in this.formData){
                    if (this.formData[key]!='' && key!='name')
                    {
                        inputText=inputText+"/"+key+": "+this.formData[key]
                    }
                }
                console.log(inputText)
                formData.append('text', inputText);
                // console.log(this.file, formData);
                postText(formData, res => {
                    console.log(res);
                    this.jump();
                });
            }
        },
        getFile(event) {
            // console.log(event.target.files);
            this.file = event.target.files[0];
            // console.log(this.file);
            event.preventDefault();
            let type = this.file.type;
            let size = this.file.size;
            // if (this.imgData.accept.indexOf(type) == -1) {
            //     ElMessage({
            //         type: 'error',
            //         message: 'Invalid Image Format',
            //     })
            // }
            let URL = window.URL || window.webkitURL;
            let imgURL = URL.createObjectURL(this.file);
            this.imgURL = imgURL;
            const dataStore = useDataStore();
            dataStore.imgFile = this.file;
        },
        submitForm(event) {
            this.$refs.img_sub.dispatchEvent(new MouseEvent('click'))

        },
        open() {
            const vm = this;
            ElMessageBox.prompt('Please add a feature', 'Feature Adding', {
                confirmButtonText: 'Add',
                cancelButtonText: 'Cancel',
                inputPattern: ''
            })
                .then(({ value }) => {
                    vm.addNFTFeature(value);
                    vm.formData[value] = null;
                    ElMessage({
                        type: 'success',
                        message: `Successfully added feature: ${value}`,
                    })
                })
        },
        showMoreSearch() {
            this.moreSearch = -this.moreSearch;
            // console.log(this.moreSearch)
        },
        addNFTFeature(featureName) {
            this.addFeature.push(featureName);
        }
    },
    created() {
        // this.drawCor();
        for (let i=0;i<10;i++)
        {
            this.conceptList.push('')
        }
    },
    mounted() {
        // this.drawCor();
    },

    // created() {
    // },
    // mounted() {
    //     // this.$refs.img_button.click(() => {
    //     //     this.$refs.img_sub.change();
    //     // })
    // },
    watch: {
        formData() {
            console.log(this.formData);
        }
    }
}

</script>
<style scoped>
.el-input {
    --el-input-border-radius: 25px;
    height: 30px;
    width:400px;
    font-size: 15px;
    font-family: Quicksand, system-ui;
    color: black
        /* padding-right: 15%; */
}

.el-form-item__content {
    background-color: #0000;
}
.axis {
  stroke: #000;
  stroke-width: 1.5px;
}

.node circle {
  stroke: #000;
}

.link {
  /* fill: none; */
  fill: blue;
  stroke: #999;
  stroke-width: 1.5px;
  stroke-opacity: .3;
}
.path {
    fill: blue
}
.link.active {
  stroke: red;
  stroke-width: 2px;
  stroke-opacity: 1;
}

.node circle.active {
  stroke: red;
  stroke-width: 3px;
}

.tooltip{
    z-index:1;
    width:300px;
    height: 300px;
    border: 1px solid;
    position: absolute;
    /* position:relative; */
    visibility: hidden;
    background-color: white;
}

#searchPrompt1 {
background: linear-gradient(90deg, green 33%, white 33%);
}
</style>
