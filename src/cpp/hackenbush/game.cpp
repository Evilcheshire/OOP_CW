#include <pybind11/embed.h>
#include <pybind11/stl.h>
#include <Python.h>
#include <vector>
#include <map>
#include <queue>
#include <algorithm>

namespace py = pybind11;
using namespace std;

class Surreal {
public:
    int val, w;
    map<int, int> frac;

    Surreal() : val(0), w(0) {}

    void clear() {
        frac.clear();
        val = w = 0;
    }

    void add(int x) {
        frac[x]++;
        auto it = frac.find(x);
        while (it != frac.end() && it->second != 1) {
            if (it->second > 1) {
                frac[it->first + 1] += it->second >> 1;
                it->second &= 1;
            }
            auto it1 = it++;
            if (!it1->second) frac.erase(it1);
        }
    }

    void divide(int x) {
        for (int i = 0; i < x; ++i) {
            if (!val) break;
            if (val & 1) add(i - w);
            val >>= 1;
        }
        w -= x;
    }

    void operator+=(const Surreal& x) {
        val += x.val;
        for (const auto& it : x.frac) {
            if (it.second) add(it.first + x.w - w);
        }
        while (!frac.empty() && frac.rbegin()->first + w >= 0) {
            if (frac.rbegin()->second) val += 1 << (frac.rbegin()->first + w);
            frac.erase(--frac.end());
        }
    }

    void solve0() {
        int p = max(1, 1 - val);
        if (frac.empty() && p + val == 1) ++p;
        val += p;
        divide(p - 1);
    }

    void solve1() {
        int p = max(1, 1 + val);
        if (val - p == -1) ++p;
        val -= p;
        divide(p - 1);
    }
};

class Game {
public:
    vector<int> id, vis;
    vector<Surreal> a;
    vector<vector<pair<int, int>>> g;
    vector<bool> is_root_vertex;

    void dfs(int u) {
        vis[u] = 1;
        for (auto& x : g[u]) {
            int v = x.first, c = x.second;
            if (vis[v]) continue;
            dfs(v);
            if (c == 0) a[id[v]].solve0();
            else a[id[v]].solve1();
            if (a[id[v]].frac.size() > a[id[u]].frac.size()) swap(id[v], id[u]);
            a[id[u]] += a[id[v]];
            a[id[v]].clear();
        }
    }

    Game(int n) : id(n + 1), vis(n + 1, 0), a(n + 1), g(n + 1), is_root_vertex(n + 1, false) {
        for (int i = 1; i <= n; ++i) id[i] = i;
    }

    void add_edge(int u, int v, int c, bool is_root = false) {
        if (u == v) return;

        auto edge_exists = [this](int u, int v, int c) {
            return any_of(g[u].begin(), g[u].end(),
                [v, c](const pair<int, int>& edge) {
                    return edge.first == v && edge.second == c;
                });
            };

        if (!edge_exists(u, v, c)) {
            g[u].emplace_back(v, c);
            g[v].emplace_back(u, c);
        }

        if (is_root) {
            is_root_vertex[u] = true;
        }
    }

    bool remove_edge(int u, int v, int color) {
        auto it = find_if(g[u].begin(), g[u].end(),
            [v, color](const pair<int, int>& edge) {
                return edge.first == v && edge.second == color;
            });
        if (it != g[u].end()) {
            g[u].erase(it);
        }
        else {
            return false;
        }

        it = find_if(g[v].begin(), g[v].end(),
            [u, color](const pair<int, int>& edge) {
                return edge.first == u && edge.second == color;
            });
        if (it != g[v].end()) {
            g[v].erase(it);
        }
        else {
            return false;
        }

        return true;
    }

    void remove_disconnected() {
        vector<bool> visited(g.size(), false);

        auto dfs = [&](int u, auto&& dfs_ref) -> void {
            visited[u] = true;
            for (auto& edge : g[u]) {
                int v = edge.first;
                if (!visited[v]) {
                    dfs_ref(v, dfs_ref);
                }
            }
            };

        for (int u = 1; u < is_root_vertex.size(); ++u) {
            if (is_root_vertex[u] && !visited[u]) {
                dfs(u, dfs);
            }
        }

        for (int u = 1; u < g.size(); ++u) {
            if (!visited[u] && !is_root_vertex[u]) {
                g[u].clear();
            }
        }

        for (int u = 0; u < g.size(); ++u) {
            g[u].erase(
                remove_if(g[u].begin(), g[u].end(),
                    [&visited](const pair<int, int>& edge) {
                        return !visited[edge.first];
                    }),
                g[u].end());
        }
    }

    void solve_game() {
        fill(vis.begin(), vis.end(), 0);

        for (int u = 1; u < is_root_vertex.size(); ++u) {
            if (is_root_vertex[u] && !vis[u]) {
                dfs(u);
            }
        }
    }

    pair<int, int> get_optimal_move() {
        Surreal best_value;
        best_value.val = -1e9;
        pair<int, int> best_move = { -1, -1 };

        for (int u = 1; u < g.size(); ++u) {
            for (auto& edge : g[u]) {
                int v = edge.first;
                int color = edge.second;

                if (color != 1) continue;

                Game temp_game = *this;

                if (temp_game.remove_edge(u, v, color)) {
                    temp_game.solve_game();

                    Surreal current_value = temp_game.a[temp_game.id[u]];

                    if (current_value.val > best_value.val) {
                        best_value = current_value;
                        best_move = { u, v };
                    }
                }
            }
        }

        return best_move;
    }

    vector<tuple<int, int, int>> get_graph() {
        vector<tuple<int, int, int>> edges;
        for (int u = 0; u < g.size(); ++u) {
            for (const auto& edge : g[u]) {
                edges.emplace_back(u, edge.first, edge.second);
            }
        }
        return edges;
    }

    void update_after_move(int u, int v, int color) {
        if (remove_edge(u, v, color)) {
            remove_disconnected();
        }
    }

    bool is_game_over(int current_color) {
        for (int u = 0; u < g.size(); ++u) {
            for (const auto& edge : g[u]) {
                if (edge.second == current_color) {
                    return false;
                }
            }
        }
        return true;
    }
};

PYBIND11_MODULE(hackenbush, m) {
    py::class_<Game>(m, "Game")
        .def(py::init<int>())
        .def("add_edge", &Game::add_edge, py::arg("u"), py::arg("v"), py::arg("c"), py::arg("is_root") = false)
        .def("remove_edge", &Game::remove_edge)
        .def("get_optimal_move", &Game::get_optimal_move)
        .def("update_after_move", &Game::update_after_move)
        .def("get_graph", &Game::get_graph)
        .def("is_game_over", &Game::is_game_over, py::arg("current_color"));
}
