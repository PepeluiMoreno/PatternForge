export function useCatalogs({ client, Entity = "{{ Entity }}", queryNames = {
  list: "{{ entities_field }}",
  get: "{{ entity_field }}",
  create: "{{ create_field }}",
  update: "{{ update_field }}",
  delete: "{{ delete_field }}",
}} = {}) {
  const listQuery = `query($search:String,$offset:Int,$limit:Int,$orderBy:String,$order:String){
    ${queryNames.list}(search:$search,offset:$offset,limit:$limit,orderBy:$orderBy,order:$order){
      id
      {% if code_field %}{{ code_field }}{% endif %}
      name
    }
  }`;
  const getQuery = `query($id:ID!){ ${queryNames.get}(id:$id){ id {% if code_field %}{{ code_field }}{% endif %} name } }`;
  const createMutation = `mutation($input:${Entity}Input!){ ${queryNames.create}(input:$input){ id {% if code_field %}{{ code_field }}{% endif %} name } }`;
  const updateMutation = `mutation($id:ID!,$input:${Entity}Input!){ ${queryNames.update}(id:$id,input:$input){ id {% if code_field %}{{ code_field }}{% endif %} name } }`;
  const deleteMutation = `mutation($id:ID!){ ${queryNames.delete}(id:$id) }`;
  async function list({ search = "", offset = 0, limit = 50, orderBy, order } = {}) {
    const data = await client.request(listQuery, { search, offset, limit, orderBy, order });
    return data[queryNames.list];
  }
  async function get(id) { const data = await client.request(getQuery, { id }); return data[queryNames.get]; }
  async function create(input) { const data = await client.request(createMutation, { input }); return data[queryNames.create]; }
  async function update(id, input) { const data = await client.request(updateMutation, { id, input }); return data[queryNames.update]; }
  async function remove(id) { const data = await client.request(deleteMutation, { id }); return !!data[queryNames.delete]; }
  return { list, get, create, update, remove };
}
