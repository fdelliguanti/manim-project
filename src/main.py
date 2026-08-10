from manim import *
import numpy as np


from manim import *

class RotatedSurface(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]), v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(4, 8)
        )
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes, sphere)
        
        intro_text = Tex(r"Imagine you want to study climate effects on earth").scale(0.75).to_edge(UP)
        self.play(Rotate(sphere, angle=TAU, axis=OUT), run_time=10, rate_func=linear)
        
class BallsIntoUrns(Scene):
    def ball_position_in_urn(self, urn, k):
        """
        Place visible balls in a small grid inside the urn.
        Only used for the first few displayed balls.
        """
        cols = 4
        row = k // cols
        col = k % cols

        x = urn.get_left()[0] + 0.25 + 0.28 * col
        y = urn.get_bottom()[1] + 0.25 + 0.18 * row
        return np.array([x, y, 0])

    def construct(self):
        # Parameters
        n = 4
        N = 16700
        S = 5000                   # number of simulations in the summary plot
        p = np.array([0.25, 0.25, 0.25, 0.25])      # uniform probabilities

        # -------------------------
        # Title and formulas
        # -------------------------
        title = Tex(r"In this video we simulate that the least number of landed balls across the urns is bounded below with high probabilty.").scale(0.75).to_edge(UP)
        description = Tex(rf"Imagine we have $n={n}$ urns and $N={N}$ balls, and we throw the balls into the urns. Each ball can land independently with probabilities $p_1={p[0]}, p_2={p[1]}, p_3={p[2]}, p_4={p[3]}$ into the four urns, respectively.").scale(0.75).next_to(title, DOWN, buff=0.2)
        formula = MathTex(
            rf"(X_1,X_2,X_3,X_4)\sim \mathrm{{Multinomial}}({N};{p[0]},{p[1]},{p[2]},{p[3]})",
        ).scale(0.75).next_to(description, DOWN)
        min_formula = MathTex(
            r"M=\min(X_1,X_2,X_3,X_4)"
        ).scale(0.8).next_to(formula, DOWN)

        self.play(Write(title))
        self.play(Write(description))
        self.play(Write(formula))
        self.play(Write(min_formula))

        # -------------------------
        # Draw the urns
        # -------------------------
        urns = VGroup(*[
            RoundedRectangle(width=1.4, height=2.2, corner_radius=0.12)
            for _ in range(n)
        ]).arrange(RIGHT, buff=0.8).next_to(min_formula, DOWN, buff=0.8)

        labels = VGroup(*[
            Tex(f"Urn {i+1}").scale(0.55).next_to(urns[i], DOWN, buff=0.15)
            for i in range(n)
        ])

        counters = VGroup(*[
            Integer(0).scale(0.65).next_to(urns[i], UP, buff=0.15)
            for i in range(n)
        ])

        self.play(Create(urns), FadeIn(labels), FadeIn(counters))

        # -------------------------
        # One trial
        # -------------------------
        counts = np.random.multinomial(N, p)

        shown = 60
        shown_assignments = np.random.choice(n, size=shown, p=p)
        running = np.zeros(n, dtype=int)

        balls = []
        for dest in shown_assignments:
            ball = Dot(radius=0.045).move_to(UP * 2.7)
            balls.append(ball)
            target = self.ball_position_in_urn(
                urns[dest],
                running[dest],
            )
            running[dest] += 1

            self.play(
                FadeIn(ball, scale=0.5),
                ball.animate.move_to(target),
                run_time=0.08,
            )

            # Update the counter after the ball lands.
            counters[dest].set_value(int(running[dest]))

        # Jump to the full result
        jump_text = Tex(rf"+ {N - shown} more balls").scale(0.65)
        jump_text.next_to(urns, LEFT, buff=0.6)

        self.play(FadeIn(jump_text))
        self.play(
            *[counters[i].animate.set_value(int(counts[i])) for i in range(n)],
            run_time=1.5
        )
        self.play(FadeOut(jump_text))

        min_value = int(counts.min())
        result_text = MathTex(
            rf"M = \min(X_1,X_2,X_3,X_4) = {min_value}"
        ).scale(0.8).next_to(formula, DOWN)
        self.play(ReplacementTransform(min_formula, result_text))
        self.wait(1.5)

        # -------------------------
        # Transition to many simulations
        # -------------------------
        self.play(
            FadeOut(urns),
            *[FadeOut(ball) for ball in balls],
            FadeOut(labels),
            FadeOut(counters),
            FadeOut(result_text),
            FadeOut(title),
            FadeOut(description),
            FadeOut(formula),
            FadeOut(min_formula),
        )

        monte_carlo_text = Tex(
            rf"Repeat the experiment $S={S}$ times and record "
            rf"$M=\min(X_1,X_2,X_3,X_4)$."
        ).scale(0.72).to_edge(UP)

        self.play(FadeIn(monte_carlo_text))

        # -------------------------
        # Run the Monte Carlo experiment
        # -------------------------
        samples = np.random.multinomial(N, p, size=S)
        minima = samples.min(axis=1)

        # Observed support of the empirical distribution
        m_min = int(minima.min())
        m_max = int(minima.max())
        m_values = np.arange(m_min, m_max + 1)

        # Empirical probability mass function:
        # P_hat(M = m) = number of occurrences of m / S
        frequencies = np.array([
            np.count_nonzero(minima == m)
            for m in m_values
        ])

        probabilities = frequencies / S

        # Choose a convenient upper limit for the probability axis.
        probability_max = float(probabilities.max())
        y_max = np.max(probability_max) #max(0.05, np.ceil(probability_max / 0.05) * 0.05)

        # Give the horizontal axis a little padding.
        x_min = m_min - 1
        x_max = m_max + 1

        axes = Axes(
            x_range=[x_min,x_max, (x_max - x_min) / 5],
            y_range=[0, y_max*1.1, y_max/5],
            x_length=10.5,
            y_length=4.0,
            tips=False,
            axis_config={
                "include_numbers": False,
                "font_size": 24,
            },
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": np.arange(
                    5 * np.ceil(x_min / 5),
                    x_max + 1,
                    np.ceil((x_max - x_min) / 5),
                ),
                "decimal_number_config": {
                    "num_decimal_places": 0,
                }
            },
            y_axis_config={
                "decimal_number_config": {
                    "num_decimal_places": 2,
                },
            },
        ).shift(DOWN * 0.45)

        for mobs in axes.x_axis.numbers:
            mobs.rotate(45/180 * PI)
            
        self.add(axes)
        x_label = MathTex("k").scale(0.7)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.15)

        distribution_label = Tex(
            "Histogram of the simulated minima for $S={S}$ Monte Carlo simulations"
        ).scale(0.62)
        distribution_label.next_to(axes, UP, buff=0.2).shift(0.5*UP)

        self.play(
            Create(axes),
            FadeIn(x_label),
            FadeIn(distribution_label),
        )

        # -------------------------
        # Construct the PMF bars
        # -------------------------
        bars = VGroup()

        # Width of one x-axis unit in scene coordinates.
        one_unit_width = np.linalg.norm(
            axes.c2p(m_min + 1, 0) - axes.c2p(m_min, 0)
        )
        bar_width = 0.8 * one_unit_width

        for m, probability in zip(m_values, probabilities):
            if probability == 0:
                continue

            bottom = axes.c2p(m, 0)
            top = axes.c2p(m, probability)
            bar_height = np.linalg.norm(top - bottom)

            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                stroke_width=1.5,
                fill_opacity=0.75,
            )

            # Rectangle positioning uses its center.
            bar.move_to((bottom + top) / 2)
            bars.add(bar)

        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars],
                lag_ratio=0.025,
            ),
            run_time=3,
        )

        # -------------------------
        # Add empirical summary statistics
        # -------------------------
        empirical_5_quantile = float(np.quantile(minima,0.05))

        quantile_line = DashedLine(
            axes.c2p(empirical_5_quantile, 0),
            axes.c2p(empirical_5_quantile, y_max*1.1),
            dash_length=0.08,
            color=YELLOW
        )

        quantile_label = MathTex(
            rf"5\% \text{{ quantile of simulated minima }} = {empirical_5_quantile:.2f}"
        ).scale(0.58)
        quantile_label.next_to(quantile_line, UP, buff=0.1)

        summary = VGroup(
            MathTex(rf"\min_i p_i={np.min(p)}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        summary.scale(0.52)
        summary.to_corner(UR, buff=0.35)
        summary.shift(DOWN * 0.8)

        self.play(
            Create(quantile_line),
            FadeIn(quantile_label),
            FadeIn(summary),
        )
        self.wait(3)

        # -------------------------
        # Transition to observe only the quantiles depending on sample size
        # -------------------------

        self.play(
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(distribution_label),
            FadeOut(bars),
            FadeOut(quantile_line),
            FadeOut(quantile_label),
            FadeOut(summary),
            FadeOut(monte_carlo_text)
        )

        transition_text = Tex(
            r"Now we observe the $5\%$ quantile of the simulated minima as a function of the number of balls $N$."
        ).scale(0.72).to_edge(UP)
        self.play(FadeIn(transition_text))
        self.wait(2)

        N_range = np.arange(1000, 20001, 1000)
        quantiles = []
        for _N in N_range:
            samples = np.random.multinomial(_N, p, size=S)
            minima = samples.min(axis=1)
            empirical_5_quantile = float(np.quantile(minima, 0.05))
            quantiles.append((_N, empirical_5_quantile))

        # Observed support of the emprical quantiles for each sample size
        quantiles = np.array(quantiles)
        q_min = int(quantiles[:, 1].min())
        q_max = int(quantiles[:, 1].max())
        q_values = np.arange(q_min, q_max + 1)
    
    
        # Choose a convenient upper limit for the probability axis.
        q_values_max = float(q_values.max())
        y_max = np.max(q_values_max)

        # Give the horizontal axis a little padding.
        x_min = N_range.min() - 1000
        x_max = N_range.max() + 1000

        
        axes = Axes(
            x_range=[x_min, x_max, (x_max - x_min) / 4],
            y_range=[0, y_max * 1.1, y_max / 5],
            x_length=10.5,
            y_length=4.0,
            tips=False,
            axis_config={
                "include_numbers": False,
                "font_size": 24,
            },
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": np.linspace(x_min, x_max, 5),
                "decimal_number_config": {
                    "num_decimal_places": 0,
                },
            },
            y_axis_config={
                "decimal_number_config": {
                    "num_decimal_places": 2,
                },
            },
        ).shift(DOWN * 0.45)

        for mob in axes.x_axis.numbers:
            mob.rotate(PI / 4)

        self.add(axes)
        
        x_label = MathTex("k").scale(0.7)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.15)

        distribution_label = Tex(
        "Distribution of empirical 5% quantiles of the simulated minima for $S={S}$ Monte Carlo simulations depending on the number of balls $N$"
        ).scale(0.62)
        distribution_label.next_to(axes, UP, buff=0.2).shift(0.5*UP)

        self.play(
            Create(axes),
            FadeIn(x_label),
            FadeIn(distribution_label),
        )

        # -------------------------
        # Construct the PMF bars
        # -------------------------
        bars = VGroup()

        # Width of one x-axis unit in scene coordinates.
        one_unit_width = np.linalg.norm(
            axes.c2p(q_min + 1, 0) - axes.c2p(q_min, 0)
        )
        bar_width = 0.8 * one_unit_width

        for (k,q) in quantiles:
            if q == 0:
                continue

            bottom = axes.c2p(k, 0)
            top = axes.c2p(k, q)
            bar_height = np.linalg.norm(top - bottom)

            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                stroke_width=1.5,
                fill_opacity=0.75,
            )

            # Rectangle positioning uses its center.
            bar.move_to((bottom + top) / 2)
            bars.add(bar)

        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars],
                lag_ratio=0.025,
            ),
            run_time=3,
        )
