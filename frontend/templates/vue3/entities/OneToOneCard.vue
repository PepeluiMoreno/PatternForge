<template><div class="pf-card"><h3>{{ Parent }} ↔ {{ Child }}</h3>
<div class="pf-actions"><input v-model="childId" placeholder="Child ID" class="pf-input"/>
<button class="pf-btn pf-primary" @click="link">Link</button>
<button class="pf-btn pf-danger" @click="unlink">Unlink</button></div>
<pre>{{ parent }}</pre><pre>{{ child }}</pre></div></template>
<script setup>
import { ref, onMounted } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props = defineProps({ endpoint:{type:String,default:""}, parentId:{type:String,required:true} });
const client = createGraphQLClient(props.endpoint); const parent = ref(null); const child = ref(null); const childId = ref("");
const GET=`query($id:ID!){ {{ parent_field_singular }}(id:$id){ id {{ child_field }}{ id } } }`;
const LINK=`mutation($parentId:ID!,$childId:ID!){ {{ link_field }}(parentId:$parentId,childId:$childId){ id } }`;
const UNLINK=`mutation($parentId:ID!){ {{ unlink_field }}(parentId:$parentId) }`;
async function load(){ const d=await client.request(GET,{id:props.parentId}); parent.value=d["{{ parent_field_singular }}"]; child.value=parent.value?.["{{ child_field }}"]??null; }
async function link(){ await client.request(LINK,{parentId:props.parentId,childId:childId.value}); await load(); }
async function unlink(){ await client.request(UNLINK,{parentId:props.parentId}); await load(); }
onMounted(load);
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-actions{display:flex;gap:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}.pf-danger{border-color:#d73a49}</style>
