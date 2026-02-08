"""Simple graph construction utilities.

The NECHTO v4.8 specification describes a rich semantic graph of
interconnected atoms.  For the purposes of this reference runtime we
employ a much simpler model: the input text is tokenised by
whitespace, each token becomes a ``SemanticAtom`` and consecutive
tokens are connected by ``Edge`` objects of type ``SUPPORTS``.

This module exposes two functions:

``parse_text_to_graph`` converts raw text into a list of atoms and a
list of edges.  Each atom is initialised with default values; harm
probability and identity alignment will be computed by the metrics
module.

``build_vector`` takes the atoms and edges produced by
``parse_text_to_graph`` and wraps them in a ``Vector`` object with a
synthetic identifier and a seed list containing the first atom.
"""

from __future__ import annotations

from typing import List, Tuple

from .types import SemanticAtom, Edge, Vector
from .metrics import harm_probability, identity_alignment


def parse_text_to_graph(text: str) -> Tuple[List[SemanticAtom], List[Edge]]:
    """Parse a plain text string into a list of semantic atoms and edges.

    The input is split on whitespace.  A ``SemanticAtom`` is created
    for each token.  Consecutive tokens are connected by an ``Edge``.
    Harm and identity metrics are computed immediately to avoid
    undefined fields later on.  Tags are initialised with a single
    ``WITNESS`` entry to indicate that each atom corresponds to a
    directly observed piece of the input.

    Args:
        text: Raw user input.

    Returns:
        A tuple ``(atoms, edges)`` where ``atoms`` is a list of
        ``SemanticAtom`` instances and ``edges`` is a list of
        ``Edge`` instances connecting them.
    """
    tokens = [tok for tok in text.strip().split() if tok]
    atoms: List[SemanticAtom] = []
    edges: List[Edge] = []
    for idx, token in enumerate(tokens):
        atom_id = f"n{idx}"
        atom = SemanticAtom(id=atom_id, label=token)
        # Default tag indicates the token is directly witnessed.
        atom.tags.append("WITNESS")
        # Compute harm and identity immediately.
        atom.harm_probability = harm_probability(atom, [])
        atom.identity_alignment = identity_alignment(atom)
        atoms.append(atom)
        # Connect to previous token if present.
        if idx > 0:
            edges.append(Edge(from_node=f"n{idx-1}", to_node=atom_id, type="SUPPORTS", weight=1.0))
    return atoms, edges


def build_vector(atoms: List[SemanticAtom], edges: List[Edge]) -> Vector:
    """Construct a single ``Vector`` from atoms and edges.

    In this minimal runtime we create only one attention vector per
    measurement.  The vector's ID is fixed to ``"V0"`` and the seed
    list contains the first atom's ID if available.  All supplied
    atoms and edges are attached to the vector.

    Args:
        atoms: List of semantic atoms.
        edges: List of edges between the atoms.

    Returns:
        A ``Vector`` ready for measurement.
    """
    seed = [atoms[0].id] if atoms else []
    return Vector(id="V0", seed_nodes=seed, nodes=atoms, edges=edges)
