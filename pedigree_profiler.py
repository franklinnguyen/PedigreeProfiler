import matplotlib.pyplot as plt


class Individual:
    def __init__(
        self, id_number, sex, affected, mother=None, father=None, children=None
    ):
        """
        Initializes an individual with the given attributes.

        Args:
            id_number (int or str): The unique identifier for the individual.
            sex (str): The sex of the individual. Can be 'M' for male or 'F' for female.
            affected (bool): The affected status of the individual.
            mother (Individual, optional): The mother of the individual. Defaults to None.
            father (Individual, optional): The father of the individual. Defaults to None.
            children (list, optional): The list of children of the individual. Defaults to an empty list.
        """
        self.id = id_number
        self.sex = sex
        self.affected = affected
        self.mother = mother
        self.father = father
        self.children = children if children is not None else []

    def add_parent_child_relationship(self, parent, sex):
        """
        Establishes a parent-child relationship between the individual and a parent.

        Args:
            parent (Individual): The parent to be added.
            sex (str): The sex of the parent. Can be 'M' for male or 'F' for female.
        """
        if sex == "M":
            self.father = parent
            parent.children.append(self)  # Add self as a child to the parent
        elif sex == "F":
            self.mother = parent
            parent.children.append(self)  # Add self as a child to the parent

    def get_children(self):
        """
        Returns the list of children of the individual.

        Returns:
            list: The list of children.
        """
        return self.children

    def get_ancestors(self, ancestors=None):
        """
        Returns the list of ancestors of the individual.

        Args:
            ancestors (list, optional): The list of ancestors. Defaults to an empty list.

        Returns:
            list: The list of ancestors.
        """
        if ancestors is None:
            ancestors = []
        if self.mother:
            ancestors.append(self.mother)
            self.mother.get_ancestors(ancestors)
        if self.father:
            ancestors.append(self.father)
            self.father.get_ancestors(ancestors)
        return ancestors

    def get_generation(self):
        """
        Returns the generation of the individual based on their parents.

        Returns:
            int: The generation of the individual.
        """
        if self.mother or self.father:
            mother_generation = self.mother.get_generation() if self.mother else 0
            father_generation = self.father.get_generation() if self.father else 0
            return max(mother_generation, father_generation) + 1
        return 0

    def is_carrier(self):
        """
        Determines whether an individual could potentially be a carrier.

        An individual could potentially be a carrier in the following situations:
        - The individual is unaffected but has at least one affected child.
        - Both parents are unaffected but the individual has an affected sibling.

        Returns:
            bool or None: True if the individual could be a carrier, False otherwise, None if it is indeterminable.
        """
        # No parents
        if not self.mother or not self.father:
            return None

        # No children
        if not self.children:
            return None

        # Unaffected female with affected child and unaffected father
        if (
            self.sex == "F"
            and not self.affected
            and any(
                child.affected and not child.father.affected for child in self.children
            )
        ):
            return True

        # Unaffected male with affected child and unaffected mother
        if (
            self.sex == "M"
            and not self.affected
            and any(
                child.affected and not child.mother.affected for child in self.children
            )
        ):
            return True

        # Unaffected with affected sibling and unaffected parents
        if (
            not self.affected
            and not self.mother.affected
            and not self.father.affected
            and any(
                sibling.affected
                for sibling in self.mother.children + self.father.children
                if sibling != self
            )
        ):
            return True

        return False


class Pedigree:
    def __init__(self, individuals=None):
        self.individuals = [] if individuals is None else individuals

    def find_affected(self):
        """
        Returns the list of affected individuals in the pedigree.

        Returns:
            list: The list of affected individuals.
        """
        return [individual for individual in self.individuals if individual.affected]

    def find_unaffected(self):
        """
        Returns the list of unaffected individuals in the pedigree.

        Returns:
            list: The list of unaffected individuals.
        """
        return [
            individual for individual in self.individuals if not individual.affected
        ]

    def find_mode_of_inheritance(self):
        """
        Determine the possible mode(s) of inheritance of a trait in a pedigree.

        This method traverses all affected individuals in a given pedigree. The inheritance modes evaluated are:
        'Autosomal Dominant', 'Autosomal Recessive', 'X-Linked Dominant', and 'X-Linked Recessive'.

        The method performs a set of checks to discard impossible modes of inheritance for each affected individual:
        - If both parents are unaffected, it discards 'Autosomal Dominant' and 'X-Linked Dominant'.
        - If one parent is unaffected and not a carrier, it discards 'Autosomal Recessive'.
        - If the individual is male and the mother is neither affected nor a carrier, it discards 'X-linked recessive'.

        If only one mode of inheritance remains possible after the evaluation of all individuals, that mode is returned.
        If more than one mode remains possible, it returns a set of all possible modes.

        Returns:
            str or set: The remaining possible mode(s) of inheritance. It returns a string if only one mode is possible, or a set of strings if multiple modes are possible.
        """

        possible_modes = {
            "Autosomal Dominant",
            "Autosomal Recessive",
            "X-Linked Dominant",
            "X-Linked Recessive",
        }

        for individual in self.find_affected():
            if individual.father and individual.mother:
                # If both parents unaffected, rule out Autosomal Dominant and X-Linked Dominant
                if not individual.father.affected and not individual.mother.affected:
                    possible_modes.discard("Autosomal Dominant")
                    possible_modes.discard("X-Linked Dominant")

                # If one parent is unaffected and not a carrier, rule out Autosomal Recessive
                if (
                    not individual.father.affected
                    and not individual.father.is_carrier()
                ) or (
                    not individual.mother.affected
                    and not individual.mother.is_carrier()
                ):
                    possible_modes.discard("Autosomal Recessive")

                # If individual is male and mother is neither affected nor a carrier, rule out X-linked recessive
                if individual.sex == "M" and not (
                    individual.mother.affected or individual.mother.is_carrier()
                ):
                    possible_modes.discard("X-Linked Recessive")

        if len(possible_modes) == 1:
            return possible_modes.pop()
        return possible_modes

    def visualize_pedigree(self):
        """
        Visualizes the pedigree using matplotlib.
        """
        # Sort individuals
        individuals = sorted(self.individuals, key=lambda x: int(x.id[1:]))

        plt.figure(figsize=(8, 6))
        ax = plt.gca()
        ax.set_aspect("equal")

        max_generations = max(
            [individual.get_generation() for individual in individuals]
        )
        id_to_index = {
            individual.id: index for index, individual in enumerate(individuals)
        }

        for index, individual in enumerate(individuals):
            x = index
            y = max_generations - individual.get_generation()

            if individual.sex == "M":
                if individual.affected:
                    shape = plt.Circle((x, y), radius=0.5, color="black")
                else:
                    shape = plt.Circle(
                        (x, y),
                        radius=0.5,
                        edgecolor="black",
                        facecolor="white",
                        linewidth=2,
                    )
            else:
                if individual.affected:
                    shape = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color="black")
                else:
                    shape = plt.Rectangle(
                        (x - 0.5, y - 0.5),
                        1,
                        1,
                        edgecolor="black",
                        facecolor="white",
                        linewidth=2,
                    )

            ax.add_patch(shape)

            if individual.mother:
                x_mom = id_to_index[individual.mother.id]
                y_mom = max_generations - individual.mother.get_generation()
                plt.plot([x, x_mom], [y, y_mom], "-")

            if individual.father:
                x_dad = id_to_index[individual.father.id]
                y_dad = max_generations - individual.father.get_generation()
                plt.plot([x, x_dad], [y, y_dad], "-")

        plt.xlim(-1, len(individuals))  # Extend x-axis
        plt.ylim(-1, max_generations + 1)
        plt.gca().invert_yaxis()
        plt.show()


if __name__ == "__main__":
    # Test Pedigree 9 - Autosomal Recessive
    I1 = Individual("I1", "M", False)
    I2 = Individual("I2", "F", False)
    I3 = Individual("I3", "F", False)
    I4 = Individual("I4", "M", False)
    I5 = Individual("I5", "F", True)
    I6 = Individual("I6", "M", False)
    I7 = Individual("I7", "F", False)
    I8 = Individual("I8", "M", True)
    I9 = Individual("I9", "F", False)
    I10 = Individual("I10", "M", False)
    I11 = Individual("I11", "F", True)
    I12 = Individual("I12", "M", False)

    # Add parent-child relationships
    I3.add_parent_child_relationship(I1, "M")
    I3.add_parent_child_relationship(I2, "F")
    I4.add_parent_child_relationship(I1, "M")
    I4.add_parent_child_relationship(I2, "F")
    I5.add_parent_child_relationship(I3, "F")
    I5.add_parent_child_relationship(I4, "M")
    I6.add_parent_child_relationship(I3, "F")
    I6.add_parent_child_relationship(I4, "M")
    I7.add_parent_child_relationship(I3, "F")
    I7.add_parent_child_relationship(I4, "M")
    I8.add_parent_child_relationship(I5, "F")
    I9.add_parent_child_relationship(I5, "F")
    I10.add_parent_child_relationship(I5, "F")
    I11.add_parent_child_relationship(I6, "M")
    I12.add_parent_child_relationship(I7, "F")

    individuals_9 = [I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12]
    pedigree9 = Pedigree(individuals_9)
    print(pedigree9.find_mode_of_inheritance())
    # pedigree9.visualize_pedigree()

    # Test Pedigree 10 - X-Linked Dominant
    I1 = Individual("I1", "M", False)
    I2 = Individual("I2", "F", True)
    I3 = Individual("I3", "F", False)
    I4 = Individual("I4", "M", False)
    I5 = Individual("I5", "F", True)
    I6 = Individual("I6", "M", False)
    I7 = Individual("I7", "F", True)
    I8 = Individual("I8", "F", False)
    I9 = Individual("I9", "M", False)
    I10 = Individual("I10", "F", True)
    I11 = Individual("I11", "M", False)
    I12 = Individual("I12", "F", True)

    # Add parent-child relationships
    I3.add_parent_child_relationship(I1, "M")
    I3.add_parent_child_relationship(I2, "F")
    I4.add_parent_child_relationship(I1, "M")
    I4.add_parent_child_relationship(I2, "F")
    I5.add_parent_child_relationship(I2, "F")
    I6.add_parent_child_relationship(I3, "F")
    I7.add_parent_child_relationship(I3, "F")
    I8.add_parent_child_relationship(I4, "M")
    I9.add_parent_child_relationship(I4, "M")
    I10.add_parent_child_relationship(I5, "F")
    I11.add_parent_child_relationship(I6, "F")
    I12.add_parent_child_relationship(I7, "F")

    individuals_10 = [I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12]
    pedigree10 = Pedigree(individuals_10)
    print(pedigree10.find_mode_of_inheritance())
    pedigree10.visualize_pedigree()

    # Test Pedigree 11 - Autosomal Dominant
    I1 = Individual("I1", "M", True)
    I2 = Individual("I2", "F", False)
    I3 = Individual("I3", "F", True)
    I4 = Individual("I4", "M", False)
    I5 = Individual("I5", "M", True)
    I6 = Individual("I6", "F", False)
    I7 = Individual("I7", "M", True)
    I8 = Individual("I8", "F", False)
    I9 = Individual("I9", "M", True)
    I10 = Individual("I10", "F", False)
    I11 = Individual("I11", "M", True)
    I12 = Individual("I12", "F", False)

    I3.add_parent_child_relationship(I1, "M")
    I3.add_parent_child_relationship(I2, "F")
    I4.add_parent_child_relationship(I1, "M")
    I4.add_parent_child_relationship(I2, "F")
    I5.add_parent_child_relationship(I3, "F")
    I6.add_parent_child_relationship(I4, "M")
    I7.add_parent_child_relationship(I3, "F")
    I8.add_parent_child_relationship(I4, "M")
    I9.add_parent_child_relationship(I5, "M")
    I10.add_parent_child_relationship(I6, "F")
    I11.add_parent_child_relationship(I7, "M")
    I12.add_parent_child_relationship(I8, "F")

    individuals_11 = [I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12]
    pedigree11 = Pedigree(individuals_11)
    print(pedigree11.find_mode_of_inheritance())

    # Test Pedigree 12 - X-Linked Recessive
    I1 = Individual("I1", "F", False)
    I2 = Individual("I2", "M", True)
    I3 = Individual("I3", "M", False)
    I4 = Individual("I4", "F", False)
    I5 = Individual("I5", "M", True)
    I6 = Individual("I6", "F", False)
    I7 = Individual("I7", "M", False)
    I8 = Individual("I8", "F", False)
    I9 = Individual("I9", "M", True)
    I10 = Individual("I10", "F", False)
    I11 = Individual("I11", "M", False)
    I12 = Individual("I12", "F", False)

    I3.add_parent_child_relationship(I1, "F")
    I3.add_parent_child_relationship(I2, "M")
    I4.add_parent_child_relationship(I1, "F")
    I4.add_parent_child_relationship(I2, "M")
    I5.add_parent_child_relationship(I4, "F")
    I6.add_parent_child_relationship(I3, "M")
    I7.add_parent_child_relationship(I3, "M")
    I8.add_parent_child_relationship(I4, "F")
    I9.add_parent_child_relationship(I6, "F")
    I10.add_parent_child_relationship(I7, "M")
    I11.add_parent_child_relationship(I8, "F")
    I12.add_parent_child_relationship(I8, "F")

    individuals_12 = [I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12]
    pedigree12 = Pedigree(individuals_12)
    print(pedigree12.find_mode_of_inheritance())
