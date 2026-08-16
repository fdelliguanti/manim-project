from manim import *
import numpy as np


from manim import *

def vec_to_tex_str(vec = [1,2,3], name="X", num_decimal = 2):
    """
    Convert a matrix to a LaTeX matrix representation.
    """
    str_to_tex = ""
    len_vec = len(vec)
    for k, e in enumerate(vec):
        if k < len_vec - 1:
            str_to_tex += f"{round(e, num_decimal)} \\\\"
        elif k == len_vec - 1:
            str_to_tex += f"{round(e,num_decimal)}"
            
    return f"{name} = \\begin{{pmatrix}} " + str_to_tex + "\\end{pmatrix}"
    
class Means(VGroup):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.title = Tex(r"Imagine you have the temperature data of 4 regions").scale(0.75).to_edge(UP)
                
        self.random_data_1 = np.random.standard_normal(8)
        self.random_data_2 = np.random.standard_normal(8)
        #self.vec_1 = Matrix([[round(k, 2)] for k in self.random_data_1]).scale(0.75).to_edge(UP, buff=2)
        #self.vec_2 = Matrix([[round(k, 2)] for k in self.random_data_2]).scale(0.75).next_to(self.vec_1, RIGHT, buff=1)
        self.vec_1 = [round(k, 2) for k in self.random_data_1]
        self.vec_2 = [round(k, 2) for k in self.random_data_2]
        
        self.x_1_label = Tex(rf"${vec_to_tex_str(self.vec_1, "X_1")} $").scale(0.75).to_edge(UP, buff=2)
        self.x_2_label = Tex(rf"${vec_to_tex_str(self.vec_2, "X_2")} $").scale(0.75).next_to(self.x_1_label, RIGHT, buff=0.5)
        
        self.mean_1 = Tex(rf"$\overline{{X}}_1$={round(np.mean(self.random_data_1), 2)}").scale(0.75).next_to(self.x_1_label, DOWN, buff=0.5)
        self.mean_2 = Tex(rf"$\overline{{X}}_2$={round(np.mean(self.random_data_2), 2)}").scale(0.75).next_to(self.x_2_label, DOWN, buff=0.5)
        
        self.gr = VGroup(self.x_1_label,self.x_2_label, self.mean_1, self.mean_2)
        
        self.add(self.gr)
        
    def animate_to_corner(self):
        return self.gr.animate.scale(0.5).to_corner(DR)

        
class Intro(ThreeDScene):
    def construct(self):
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        title = Tex(r"Imagine you want to study climate change on earth").scale(0.75).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        text_before_means = []
        text_before_means.append(Tex(r"Nowadays, the global average temperature is used as indicator for the climate change.").scale(0.75).next_to(title, DOWN, buff = 0.5))
        text_before_means.append(Tex(r"But what does it mean? How to assign a planet one number that should represent somehow its temperature?").scale(0.75).next_to(text_before_means[-1],DOWN, buff = 0.2))
        text_before_means.append(Tex(r"The definition of 'global average temperature' can vary. One example is the gloabel surface temperature (GST) which is computed as the average of the temperature at the surface layer of the ocean and over land (Wikipedia).").scale(0.75).next_to(text_before_means[-1],DOWN, buff = 0.2))
        
        for text in text_before_means:
            self.add_fixed_in_frame_mobjects(text)
            self.play(Write(text))
            self.wait(2)
            
        sphere = RotatedSphere().next_to(text_before_means[-1], DOWN, buff=0.5)
        self.add(sphere)
        self.play(Create(sphere))
        self.play(sphere.rotate_sphere())
        means = Means().next_to(text_before_means[-1], DOWN, buff = 0.5)
        self.add_fixed_in_frame_mobjects(means)
        self.play(Write(means))
        self.wait(2)
        self.play(means.animate_to_corner())
        self.wait(2)
        """
        texts = []
        
        texts.append(Tex(r"One way to do this is to simulate the climate effects on a model of the earth.").scale(0.75).next_to(title, DOWN, buff=0.2))
        texts.append(Tex(r"You could for example simulate whether the industrialisation had effects onto the climate by comparing pre-industrialisation and post-industrialisation scenarios.").scale(0.75).next_to(texts[-1], DOWN, buff=0.2))
        texts.append(Tex(r"One could this by just comparing the effects within a regions.").scale(0.75).next_to(texts[-1], DOWN, buff=0.2))
        texts.append(Tex(r"However, this would not be a good idea since the climate is a global phenomenon and the effects of industrialisation are not limited to one region.").scale(0.75).next_to(texts[-1], DOWN, buff=0.2))
        texts.append(Tex(r"Instead, one could simulate the climate effects on a model of the earth and compare the effects of industrialisation on the global climate.").scale(0.75).next_to(texts[-1], DOWN, buff=0.2))
        texts.append(Tex(r"But there is not the 'global wheter station' that measures the global climate.").scale(0.75).next_to(texts[-1], DOWN, buff=0.2))
        texts.append(Tex(r"Instead, we have to rely on the measurements of many local weather stations, which can be viewed as proxies for their regions and combine them to get a global picture.").scale(0.75).next_to(texts[-1], DOWN, buff=0.2))
        for text in texts:
            self.play(Write(text))
            self.wait(2)
        """
        
from manim import *
import numpy as np


from manim import *

import numpy as np
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image


class RotatingEarth(ThreeDScene):
    PRECISION = 0.1
    EARTH_URL = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/"
        "Whole_world_-_land_and_oceans.jpg/"
        "1280px-Whole_world_-_land_and_oceans.jpg"
    )

    EARTH_FILE = Path("assets") / "earth.jpg"

    # Globe settings
    RADIUS = 3.0

    # Number of texture patches.
    #
    # Higher values -> better image quality, slower rendering.
    LATITUDE_PATCHES = int(PRECISION * 100)
    LONGITUDE_PATCHES = int(PRECISION * 100)

    # Mesh spacing, in degrees
    LATITUDE_STEP = 15
    LONGITUDE_STEP = 15

    # ------------------------------------------------------------
    # Download Earth image
    # ------------------------------------------------------------

    @classmethod
    def download_earth_texture(cls):
        cls.EARTH_FILE.parent.mkdir(parents=True, exist_ok=True)

        if cls.EARTH_FILE.exists():
            print(f"Using cached Earth texture: {cls.EARTH_FILE}")
            return cls.EARTH_FILE

        print("Downloading Earth texture...")

        # Wikimedia can reject requests without a User-Agent.
        request = Request(
            cls.EARTH_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 ManimCE RotatingEarth example"
                )
            },
        )

        with urlopen(request) as response:
            image_data = response.read()

        cls.EARTH_FILE.write_bytes(image_data)

        print(f"Saved Earth texture to: {cls.EARTH_FILE}")

        return cls.EARTH_FILE

    # ------------------------------------------------------------
    # Spherical coordinates
    # ------------------------------------------------------------

    @staticmethod
    def sphere_point(theta, phi, radius):
        """
        theta:
            longitude angle, 0 ... 2π

        phi:
            polar angle, 0 ... π

            0   = north pole
            π/2 = equator
            π   = south pole
        """

        return radius * np.array(
            [
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi),
            ]
        )

    # ------------------------------------------------------------
    # Build textured sphere
    # ------------------------------------------------------------

    def create_textured_earth(self, image_path):
        image = Image.open(image_path).convert("RGB")

        image_width, image_height = image.size

        earth = VGroup()

        n_lat = self.LATITUDE_PATCHES
        n_lon = self.LONGITUDE_PATCHES

        for i in range(n_lat):
            # Polar coordinate limits
            phi_1 = PI * i / n_lat
            phi_2 = PI * (i + 1) / n_lat

            # Sample at center of patch
            phi_center = (phi_1 + phi_2) / 2

            # Convert latitude position to image Y coordinate.
            image_y = int(
                (phi_center / PI) * (image_height - 1)
            )

            for j in range(n_lon):

                theta_1 = TAU * j / n_lon
                theta_2 = TAU * (j + 1) / n_lon

                theta_center = (theta_1 + theta_2) / 2

                # ------------------------------------------------
                # Texture-coordinate correction
                #
                # Depending on the map, you may want to add PI
                # here to rotate the continents around the globe.
                # ------------------------------------------------

                texture_theta = theta_center + PI

                texture_theta %= TAU

                image_x = int(
                    (texture_theta / TAU)
                    * (image_width - 1)
                )

                r, g, b = image.getpixel((image_x, image_y))

                patch_color = ManimColor.from_rgb(
                    (
                        r / 255,
                        g / 255,
                        b / 255,
                    )
                )

                # Each Surface represents one small patch
                # of the Earth texture.
                patch = Surface(
                    lambda u, v: self.sphere_point(
                        u,
                        v,
                        self.RADIUS,
                    ),
                    u_range=[theta_1, theta_2],
                    v_range=[phi_1, phi_2],
                    resolution=(1, 1),
                    fill_color=patch_color,
                    checkerboard_colors=False,
                    fill_opacity=1,
                    stroke_width=0,
                )

                earth.add(patch)

        return earth

    # ------------------------------------------------------------
    # Latitude / longitude mesh
    # ------------------------------------------------------------

    def create_earth_mesh(self):
        mesh = VGroup()

        radius = self.RADIUS * 1.002

        # --------------------------------------------------------
        # Latitude lines
        # --------------------------------------------------------

        for latitude in range(
            -75,
            90,
            self.LATITUDE_STEP,
        ):
            lat = latitude * DEGREES

            # Convert latitude to polar angle.
            phi = PI / 2 - lat

            latitude_line = ParametricFunction(
                lambda theta, phi=phi: self.sphere_point(
                    theta,
                    phi,
                    radius,
                ),
                t_range=[0, TAU],
                color=WHITE,
                stroke_width=0.7,
            )

            latitude_line.set_opacity(0.35)

            mesh.add(latitude_line)

        # --------------------------------------------------------
        # Longitude lines
        # --------------------------------------------------------

        for longitude in range(
            0,
            360,
            self.LONGITUDE_STEP,
        ):
            theta = longitude * DEGREES

            longitude_line = ParametricFunction(
                lambda phi, theta=theta: self.sphere_point(
                    theta,
                    phi,
                    radius,
                ),
                t_range=[0, PI],
                color=WHITE,
                stroke_width=0.7,
            )

            longitude_line.set_opacity(0.35)

            mesh.add(longitude_line)

        return mesh

    # ------------------------------------------------------------
    # Scene
    # ------------------------------------------------------------

    def construct(self):

        # --------------------------------------------------------
        # Get texture
        # --------------------------------------------------------
      
        texture_file = self.download_earth_texture()

        # --------------------------------------------------------
        # Camera
        # --------------------------------------------------------

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-30 * DEGREES,
            zoom=0.8,
        )

        # --------------------------------------------------------
        # Earth
        # --------------------------------------------------------

        earth = self.create_textured_earth(texture_file)

        #mesh = self.create_earth_mesh()

        globe = VGroup(
            earth,
            #mesh,
        )

        # Slight tilt of Earth's rotation axis.
        
        globe.rotate(
            23.5 * DEGREES,
            axis=RIGHT,
        )
        
        # --------------------------------------------------------
        # Appearance
        # --------------------------------------------------------

        self.play(
            FadeIn(earth),
            #Create(mesh),
            run_time=2,
        )

        self.wait(0.5)

        # --------------------------------------------------------
        # Rotate Earth
        # --------------------------------------------------------

        self.play(
            Rotate(
                globe,
                angle=TAU,
                axis=np.cos(23.5*DEGREES)*OUT-np.sin(23.5*DEGREES)*UP,
                #about_point=ORIGIN,
                rate_func=linear,
            ),
            run_time=12,
        )

        self.wait()

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
