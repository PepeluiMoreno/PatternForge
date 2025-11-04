<template><div class="pf-card"><h3>{{ OwnerEntity }} Attachments</h3>
<div class="pf-toolbar"><input v-model="ownerId" placeholder="Owner ID" class="pf-input"/><input v-model="attachmentId" placeholder="Attachment ID" class="pf-input"/><button class="pf-btn pf-primary" @click="attach">Attach</button></div>
<ul class="pf-grid"><li v-for="a in rows" :key="a.id" class="pf-tile"><a :href="a.url" target="_blank">{{ a.url }}</a><br/><small>{{ a.mimeType }} – {{ a.sizeBytes || "?" }} bytes</small><br/><button class="pf-btn pf-danger" @click="detach(a.id)">Detach</button></li></ul></div></template>
<script setup>
import { ref, watch } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""}, id:{type:String,required:false} }); const client=createGraphQLClient(props.endpoint);
const ownerId=ref(props.id||""); const attachmentId=ref(""); const rows=ref([]);
const Q=`query($id:ID!){ {{ owner_field_singular }}(id:$id){ id attachments{ id url mimeType sizeBytes } } }`;
const M={ attach:`mutation($ownerId:ID!,$attachmentId:ID!){ {{ attach_field }}(ownerId:$ownerId,attachmentId:$attachmentId) }`, detach:`mutation($ownerId:ID!,$attachmentId:ID!){ {{ detach_field }}(ownerId:$ownerId,attachmentId:$attachmentId) }` };
async function load(){ if(!ownerId.value){ rows.value=[]; return; } const d=await client.request(Q,{id:ownerId.value}); rows.value=d["{{ owner_field_singular }}"]?.attachments??[]; }
async function attach(){ await client.request(M.attach,{ownerId:ownerId.value,attachmentId:attachmentId.value}); await load(); }
async function detach(attId){ await client.request(M.detach,{ownerId:ownerId.value,attachmentId:attId}); await load(); }
watch(ownerId,load,{immediate:true});
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}.pf-danger{border-color:#d73a49}.pf-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;padding:0;list-style:none}.pf-tile{border:1px solid #eee;border-radius:10px;padding:10px;background:#fff}</style>
