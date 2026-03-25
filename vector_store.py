import faiss
import numpy as np
import os
import json


class VideoDatabase:
    def __init__(self, index_path="faiss_index.index", metadata_path="metadata.json", dim=2048):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dim = dim
        self.index = None
        self.metadata = []
        self._load_or_create()

    def _load_or_create(self):
        """Load existing index or create new one"""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, "r") as f:
                    self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatIP(self.dim)

    def _save(self):
        """Save index and metadata"""
        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f)

    def add_video(self, features, token, owner, video_path):
        """
        Add video features to database
        features: numpy array (n_frames, 2048)
        """

        if features is None or len(features) == 0:
            return False

        if features.shape[1] != self.dim:
            raise ValueError(f"Feature dimension must be {self.dim}")

        features = features.astype("float32")

        
        faiss.normalize_L2(features)

        for feature in features:
            feature = feature.reshape(1, -1)

            
            self.index.add(feature)

            
            self.metadata.append({
                "token": token,
                "owner": owner,
                "video_path": video_path
            })

        self._save()
        return True

    def search(self, query_features, threshold=0.85, k=5):
        """
        Search similar videos
        """

        if self.index.ntotal == 0:
            return []

        if query_features.shape[1] != self.dim:
            raise ValueError(f"Query dimension must be {self.dim}")

        query_features = query_features.astype("float32")

        
        faiss.normalize_L2(query_features)

        k = min(k, self.index.ntotal)

        distances, indices = self.index.search(query_features, k)

        best_matches = {}

        for i, idx in enumerate(indices[0]):

            if idx == -1:
                continue

            score = float(distances[0][i])

            if score < threshold:
                continue

            if idx >= len(self.metadata):
                continue

            meta = self.metadata[idx]
            token = meta["token"]

            
            if token not in best_matches or score > best_matches[token]["confidence"]:
                best_matches[token] = {
                    "token": token,
                    "owner": meta["owner"],
                    "confidence": round(score * 100, 2),
                    "video_path": meta["video_path"]
                }

        return list(best_matches.values())