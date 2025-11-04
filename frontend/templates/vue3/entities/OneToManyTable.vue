<template><div class="pf-card"><h3>{{ Parent }} → {{ Child }}</h3>
<div class="pf-toolbar"><input v-model="addId" placeholder="Child ID" class="pf-input"/><button class="pf-btn pf-primary" @click="attach">Attach</button></div>
<table class="pf-table"><thead><tr><th>Child ID</th><th class="pf-right">Actions</th></tr></thead>
<tbody><tr v-for="row in rows" :key="row.id"><td>{{ row.id }}</td><td class="pf-right"><button class="pf-btn pf-danger" @click="detach(row.id)">Detach</button></td></tr></tbody></table></div></template>
<script setup>
import { ref, onMounted } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props = defineProps({ endpoint:{type:String,default:""}, parentId:{type:String,required:true} });
const client=createGraphQLClient(props.endpoint); const rows=ref([]); const addId=ref("");
const Q=`query($id:ID!){ {{ parent_field_singular }}(id:$id){ id {{ children_field }}{ id } } }`;
const M={ attach:`mutation($parentId:ID!,$childId:ID!){ {{ attach_field }}(parentId:$parentId, childId:$childId){ id } }`, detach:`mutation($childId:ID!){ {{ detach_field }}(childId:$childId) }` };
async function load(){ const d=await client.request(Q,{id:props.parentId}); rows.value=d["{{ parent_field_singular }}"]?.["{{ children_field }}"]??[]; }
async function attach(){ await client.request(M.attach,{parentId:props.parentId,childId:addId.value}); await load(); }
async function detach(childId){ await client.request(M.detach,{childId}); await load(); }
onMounted(load);
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}.pf-danger{border-color:#d73a49}.pf-table{width:100%;border-collapse:collapse}.pf-table th,.pf-table td{border-bottom:1px solid #eee;padding:8px}.pf-right{text-align:right}</style>
