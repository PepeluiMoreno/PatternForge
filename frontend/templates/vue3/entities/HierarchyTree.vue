<template><div class="pf-card"><h3>{{ Node }} Tree</h3>
<ul class="pf-tree"><TreeNode v-for="n in roots" :key="n.id" :node="n" :load-children="loadChildren"/></ul></div></template>
<script setup>
import { ref, defineComponent } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props = defineProps({ endpoint:{type:String,default:""} }); const client=createGraphQLClient(props.endpoint);
const roots=ref([]); const ROOTS=`query{ {{ nodes_field }}{ id } }`; const CHILDREN=`query($id:ID!){ {{ node_field }}(id:$id){ id children{ id } } }`;
async function loadRoots(){ const d=await client.request(ROOTS); roots.value=d["{{ nodes_field }}"]; }
async function loadChildren(id){ const d=await client.request(CHILDREN,{id}); return d["{{ node_field }}"]?.children??[]; }
const TreeNode=defineComponent({ name:"TreeNode", props:{node:Object,loadChildren:Function}, data(){return{expanded:false,kids:[]}}, methods:{async toggle(){ this.expanded=!this.expanded; if(this.expanded&&this.kids.length===0){ this.kids=await this.loadChildren(this.node.id); } }}, template:`
<li><button class="pf-btn" @click="toggle()">{{ expanded ? "-" : "+" }}</button><span class="pf-node">{{ node.id }}</span>
<ul v-if="expanded"><TreeNode v-for="k in kids" :key="k.id" :node="k" :load-children="loadChildren"/></ul></li>` });
loadRoots();
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-tree{list-style:none;padding-left:0}.pf-btn{padding:2px 8px;margin-right:6px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-node{padding:4px 8px}ul{margin:0 0 0 16px;padding:0}</style>
