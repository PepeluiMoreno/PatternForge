<template><div class="pf-card"><h3>{{ Entity }} Connection</h3>
<div class="pf-toolbar"><input v-model="search" placeholder="Search..." class="pf-input"/><select v-model="orderBy" class="pf-input"><option value="">(none)</option><option v-for="c in sortable" :key="c" :value="c">{{ c }}</option></select><select v-model="order" class="pf-input"><option>ASC</option><option>DESC</option></select><button class="pf-btn" @click="reload">Load</button></div>
<ul><li v-for="e in edges" :key="e.cursor">{{ e.node.id }} – {{ e.cursor }}</li></ul>
<div class="pf-footer"><button class="pf-btn" :disabled="!pageInfo.hasNextPage" @click="next">Next</button><small>EndCursor: {{ pageInfo.endCursor || "-" }}</small></div></div></template>
<script setup>
import { ref } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""}, sortable:{type:Array,default:()=>["name","created_at","updated_at"]} });
const client=createGraphQLClient(props.endpoint); const edges=ref([]); const pageInfo=ref({hasNextPage:false,endCursor:null}); const search=ref(""); const orderBy=ref(""); const order=ref("ASC"); const after=ref(null);
const Q=`query($after:String,$first:Int,$search:String,$orderBy:String,$order:String){ {{ entities_connection_field }}(after:$after,first:$first,search:$search,orderBy:$orderBy,order:$order){ totalCount edges{ cursor node{ id } } pageInfo{ hasNextPage endCursor } } }`;
async function load(){ const d=await client.request(Q,{after:after.value,first:20,search:search.value,orderBy:orderBy.value||null,order:order.value}); const conn=d["{{ entities_connection_field }}"]; edges.value=conn.edges; pageInfo.value=conn.pageInfo; }
function reload(){ after.value=null; load(); } function next(){ after.value=pageInfo.value.endCursor; load(); } load();
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}.pf-footer{display:flex;justify-content:space-between;margin-top:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}</style>
