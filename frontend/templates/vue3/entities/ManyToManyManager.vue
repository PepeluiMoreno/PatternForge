<template><div class="pf-card"><h3>{{ Left }} ↔ {{ Right }}</h3>
<div class="pf-toolbar"><input v-model="targetId" placeholder="Target ID" class="pf-input"/><button class="pf-btn pf-primary" @click="link">Link</button></div>
<table class="pf-table"><thead><tr><th>Linked ID</th><th class="pf-right">Actions</th></tr></thead>
<tbody><tr v-for="row in rows" :key="row.id"><td>{{ row.id }}</td><td class="pf-right"><button class="pf-btn pf-danger" @click="unlink(row.id)">Unlink</button></td></tr></tbody></table></div></template>
<script setup>
import { ref, onMounted } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props = defineProps({ endpoint:{type:String,default:""}, leftId:{type:String,required:true} });
const client=createGraphQLClient(props.endpoint); const targetId=ref(""); const rows=ref([]);
const Q=`query($id:ID!){ {{ left_field_singular }}(id:$id){ id {{ rights_field }}{ id } } }`;
const M={ link:`mutation($leftId:ID!,$rightId:ID!){ {{ link_field }}(leftId:$leftId,rightId:$rightId) }`, unlink:`mutation($leftId:ID!,$rightId:ID!){ {{ unlink_field }}(leftId:$leftId,rightId:$rightId) }` };
async function load(){ const d=await client.request(Q,{id:props.leftId}); rows.value=d["{{ left_field_singular }}"]?.["{{ rights_field }}"]??[]; }
async function link(){ await client.request(M.link,{leftId:props.leftId,rightId:targetId.value}); await load(); }
async function unlink(rightId){ await client.request(M.unlink,{leftId:props.leftId,rightId}); await load(); }
onMounted(load);
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}.pf-danger{border-color:#d73a49}.pf-table{width:100%;border-collapse:collapse}.pf-table th,.pf-table td{border-bottom:1px solid #eee;padding:8px}.pf-right{text-align:right}</style>
