export function createGraphQLClient(endpoint){
  const url = endpoint || (import.meta?.env?.VITE_GRAPHQL_ENDPOINT ?? "http://localhost:8000/graphql");
  return {
    async request(query, variables = {}){
      const res = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query, variables }) });
      const json = await res.json();
      if (json.errors) throw new Error(JSON.stringify(json.errors));
      return json.data;
    }
  };
}
