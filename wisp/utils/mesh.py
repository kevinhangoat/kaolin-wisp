


# import trimesh
# import mcubes

# def extract_fields(bound_min, bound_max, resolution, query_func, S=128):

#     X = torch.linspace(bound_min[0], bound_max[0], resolution).split(S)
#     Y = torch.linspace(bound_min[1], bound_max[1], resolution).split(S)
#     Z = torch.linspace(bound_min[2], bound_max[2], resolution).split(S)

#     u = np.zeros([resolution, resolution, resolution], dtype=np.float32)
#     with torch.no_grad():
#         for xi, xs in enumerate(X):
#             for yi, ys in enumerate(Y):
#                 for zi, zs in enumerate(Z):
#                     xx, yy, zz = custom_meshgrid(xs, ys, zs)
#                     pts = torch.cat([xx.reshape(-1, 1), yy.reshape(-1, 1), zz.reshape(-1, 1)], dim=-1) # [S, 3]
#                     val = query_func(pts).reshape(len(xs), len(ys), len(zs)).detach().cpu().numpy() # [S, 1] --> [x, y, z]
#                     u[xi * S: xi * S + len(xs), yi * S: yi * S + len(ys), zi * S: zi * S + len(zs)] = val
#     return u

# def extract_geometry(bound_min, bound_max, resolution, threshold, query_func):
#     #print('threshold: {}'.format(threshold))
#     u = extract_fields(bound_min, bound_max, resolution, query_func)

#     #print(u.shape, u.max(), u.min(), np.percentile(u, 50))
    
#     vertices, triangles = mcubes.marching_cubes(u, threshold)

#     b_max_np = bound_max.detach().cpu().numpy()
#     b_min_np = bound_min.detach().cpu().numpy()

#     vertices = vertices / (resolution - 1.0) * (b_max_np - b_min_np)[None, :] + b_min_np[None, :]
#     return vertices, triangles

# def save_mesh(self, time, save_path=None, resolution=256, threshold=10):
#     if save_path is None:
#         save_path = os.path.join(self.root, 'meshes', f'{self.name}_{self.epoch}.ply')

#     os.makedirs(os.path.dirname(save_path), exist_ok=True)

#     def query_func(pts):
#         with torch.no_grad():
#             with torch.cuda.amp.autocast(enabled=self.fp16):
#                 sigma = self.model.density(pts.to(self.device), time)['sigma']
#         return sigma

#     vertices, triangles = extract_geometry(self.model.aabb_infer[:3], self.model.aabb_infer[3:], resolution=resolution, threshold=threshold, query_func=query_func)

#     mesh = trimesh.Trimesh(vertices, triangles, process=False) # important, process=True leads to seg fault...
#     mesh.export(save_path)

#     self.log(f"==> Finished saving mesh.")