import { Box, Heading, Text, Grid, GridItem, Button } from "@chakra-ui/react";
import { Link as RouterLink, createFileRoute } from "@tanstack/react-router";
//import { Route as LayoutRoute } from "../_layout";


export const Route = createFileRoute("/_layout/dns-dashboard")({
    component: DNSDashboard, 
});

function DNSDashboard() {
    return (
        <Box p={6}>
            <Heading mb={4}>DNS Management Dashboard</Heading>
            <Text mb={6}>
                Welcome to the DNS Management Portal! Manage your DNS records with ease.
            </Text>

            <Grid templateColumns="repeat(2, 1fr)" gap={6}>
                {/* Section for DNS Records */}
                <GridItem>
                    <Box p={4} borderWidth="1px" borderRadius="lg" shadow="sm">
                        <Heading size="md" mb={2}>DNS Records</Heading>
                        <Text mb={4}>View, add, and update DNS records for your domains.</Text>
                        <Button colorScheme="teal" as={RouterLink} to="/dns-records">
                            Go to DNS Records
                        </Button>
                    </Box>
                </GridItem>

                {/* Section for Account Settings */}
                <GridItem>
                    <Box p={4} borderWidth="1px" borderRadius="lg" shadow="sm">
                        <Heading size="md" mb={2}>Account Settings</Heading>
                        <Text mb={4}>
                            Update your account information and preferences.
                        </Text>
                        <Button colorScheme="blue" as={RouterLink} to="/settings">
                            Go to Settings
                        </Button>
                    </Box>
                </GridItem>
            </Grid>
        </Box>
    );
}
