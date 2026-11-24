import matplotlib.pyplot as plt

import euclidean
import generators
import grenoble_av
import grenoble_seqav
import warszawa_av
import warszawa_seqav
import plot_cone2d
import plot_cone2d_iterations
import plot_gaussian
import plot_gaussian2d
import plot_gaussian2d_iterations
import plot_gaussian_av_second
import plot_gaussian_av_winner
import plot_gaussian_iterations
import plot_triangle
import plot_triangular2d
import plot_triangular2d_iterations
import plot_triangle_av_second
import plot_triangle_av_winner
import plot_triangle_iterations

N2 = euclidean.N_CANDIDATES_2D


def compute_all():
    print("Triangle, one sample", flush=True)
    euclidean.run_triangle().to_csv(plot_triangle.RESULT, index=False)

    print("Gaussian, one sample", flush=True)
    euclidean.run_gaussian().to_csv(plot_gaussian.RESULT, index=False)

    print("Triangle, iterations", flush=True)
    euclidean.run_iterations(generators.generate_profile_triangular).to_csv(
        plot_triangle_iterations.RESULT, index=False
    )

    print("Gaussian, iterations", flush=True)
    euclidean.run_iterations(generators.generate_profile_gaussian).to_csv(
        plot_gaussian_iterations.RESULT, index=False
    )

    print("Triangle, AV iterations", flush=True)
    winner, second = euclidean.run_av_iterations(generators.generate_profile_triangular)
    winner.to_csv(plot_triangle_av_winner.RESULT, index=False)
    second.to_csv(plot_triangle_av_second.RESULT, index=False)

    print("Gaussian, AV iterations", flush=True)
    winner, second = euclidean.run_av_iterations(generators.generate_profile_gaussian)
    winner.to_csv(plot_gaussian_av_winner.RESULT, index=False)
    second.to_csv(plot_gaussian_av_second.RESULT, index=False)

    print("Triangular 2D, one sample", flush=True)
    euclidean.run_sample(generators.generate_profile_triangular_2d, n_candidates=N2).to_csv(
        plot_triangular2d.RESULT, index=False
    )

    print("Cone 2D, one sample", flush=True)
    euclidean.run_sample(generators.generate_profile_cone_2d, n_candidates=N2).to_csv(
        plot_cone2d.RESULT, index=False
    )

    print("Gaussian 2D, one sample", flush=True)
    euclidean.run_sample(generators.generate_profile_gaussian_2d, n_candidates=N2).to_csv(
        plot_gaussian2d.RESULT, index=False
    )

    print("Triangular 2D, iterations", flush=True)
    euclidean.run_iterations(
        generators.generate_profile_triangular_2d, n_candidates=N2
    ).to_csv(plot_triangular2d_iterations.RESULT, index=False)

    print("Cone 2D, iterations", flush=True)
    euclidean.run_iterations(
        generators.generate_profile_cone_2d, n_candidates=N2
    ).to_csv(plot_cone2d_iterations.RESULT, index=False)

    print("Gaussian 2D, iterations", flush=True)
    euclidean.run_iterations(
        generators.generate_profile_gaussian_2d, n_candidates=N2
    ).to_csv(plot_gaussian2d_iterations.RESULT, index=False)


def plot_all():
    saved = [
        plot_triangle.plot(show=False),
        plot_gaussian.plot(show=False),
        plot_triangle_iterations.plot(show=False),
        plot_gaussian_iterations.plot(show=False),
        plot_triangle_av_winner.plot(show=False),
        plot_triangle_av_second.plot(show=False),
        plot_gaussian_av_winner.plot(show=False),
        plot_gaussian_av_second.plot(show=False),
        plot_triangular2d.plot(show=False),
        plot_cone2d.plot(show=False),
        plot_gaussian2d.plot(show=False),
        plot_triangular2d_iterations.plot(show=False),
        plot_cone2d_iterations.plot(show=False),
        plot_gaussian2d_iterations.plot(show=False),
        grenoble_seqav.plot(show=False),
        grenoble_av.plot(show=False),
        warszawa_seqav.plot(show=False),
        warszawa_av.plot(show=False),
    ]
    for path in saved:
        print(path, flush=True)
    plt.show()


def main():
    print("compute: 1D + 2D SeqAV (sample/iterations), 1D AV iterations")
    print("plot: those figures, Grenoble + Warszawa sequential/pairs")
    choice = input("compute or plot? ").strip().lower()
    if choice.startswith("c"):
        compute_all()
    elif choice.startswith("p"):
        plot_all()
    else:
        print("Type compute or plot.")


if __name__ == "__main__":
    main()
