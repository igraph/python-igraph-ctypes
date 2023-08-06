# Open questions

Open questions to be discussed regarding the design of the new igraph
Python interface:

- Shall we allow string representations of enums to be resolved to their
  corresponding enum values? This would make it possible to write something
  like `"directed"` instead of `Adjacency.DIRECTED`.

- Shall we allow the user to refer to vertices by strings and resolve strings
  automatically to vertex names, or do we want to force the user to indicate
  explicitly when he wants to do a by-name lookup?

- Shall we allow the user to refer to individual edges by a `(source, target)`
  tuple if it is unambiguous?

- Shall we allow the user to specify edge weight vectors simply by writing the
  name of the edge attribute storing the weights?

- Shall we treat the `weight` edge attribute implicitly as edge weights?

- Shall we allow dicts mapping vertex names to floats to be treated as a
  `VERTEX_QTY` abstract type?
