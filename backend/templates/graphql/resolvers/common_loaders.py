from aiodataloader import DataLoader

class ByIdLoader(DataLoader):
    def __init__(self, session, model):
        super().__init__()
        self.session = session
        self.model = model

    async def batch_load_fn(self, keys):
        from sqlalchemy import select
        rows = (await self.session.execute(
            select(self.model).where(self.model.id.in_(keys))
        )).scalars().all()
        by_id = {getattr(r, "id"): r for r in rows}
        return [by_id.get(k) for k in keys]


class JunctionLoader(DataLoader):
    def __init__(self, session, junction, left_fk: str, right_fk: str, side: str, target_model):
        super().__init__()
        self.session = session
        self.junction = junction
        self.left_fk = left_fk
        self.right_fk = right_fk
        self.side = side
        self.target_model = target_model

    async def batch_load_fn(self, keys):
        from sqlalchemy import select
        J = self.junction
        if self.side == "left":
            res = await self.session.execute(
                select(self.target_model).join(J, getattr(J, self.left_fk)==self.target_model.id).where(
                    getattr(J, self.right_fk).in_(keys)
                )
            )
            rows = res.scalars().all()
            from collections import defaultdict
            out = defaultdict(list)
            jres = await self.session.execute(
                select(J).where(getattr(J, self.right_fk).in_(keys))
            )
            jrows = jres.scalars().all()
            by_left = {getattr(r, "id"): r for r in rows}
            for j in jrows:
                rkey = getattr(j, self.right_fk)
                lid = getattr(j, self.left_fk)
                if lid in by_left:
                    out[rkey].append(by_left[lid])
            return [out.get(k, []) for k in keys]
        else:
            res = await self.session.execute(
                select(self.target_model).join(J, getattr(J, self.right_fk)==self.target_model.id).where(
                    getattr(J, self.left_fk).in_(keys)
                )
            )
            rows = res.scalars().all()
            from collections import defaultdict
            out = defaultdict(list)
            jres = await self.session.execute(
                select(J).where(getattr(J, self.left_fk).in_(keys))
            )
            jrows = jres.scalars().all()
            by_right = {getattr(r, "id"): r for r in rows}
            for j in jrows:
                lkey = getattr(j, self.left_fk)
                rid = getattr(j, self.right_fk)
                if rid in by_right:
                    out[lkey].append(by_right[rid])
            return [out.get(k, []) for k in keys]
