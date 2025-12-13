import { StyleSheet, Image, Platform, FlatList } from 'react-native';

import ParallaxScrollView from '@/components/parallax-scroll-view';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';

export default function TabTwoScreen() {
  const badges = [
    { id: '1', name: 'First Steps', icon: 'star.fill', color: '#FCD34D', desc: 'Completed your first lesson' },
    { id: '2', name: 'Math Whiz', icon: 'number', color: '#60A5FA', desc: ' scored 100% in Math' },
    { id: '3', name: 'Bookworm', icon: 'book.fill', color: '#F472B6', desc: 'Read 5 lessons' },
  ];

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={
        <IconSymbol
          size={310}
          color="#808080"
          name="trophy.fill"
          style={styles.headerImage}
        />
      }>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Achievements</ThemedText>
      </ThemedView>
      <ThemedText>Earn badges by learning and taking quizzes!</ThemedText>

      {badges.map((badge) => (
        <ThemedView key={badge.id} style={styles.badgeCard}>
          <IconSymbol size={40} name={badge.icon as any} color={badge.color} style={{ marginRight: 16 }} />
          <ThemedView style={{ flex: 1 }}>
            <ThemedText type="subtitle">{badge.name}</ThemedText>
            <ThemedText>{badge.desc}</ThemedText>
          </ThemedView>
        </ThemedView>
      ))}

    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerImage: {
    color: '#808080',
    bottom: -90,
    left: -35,
    position: 'absolute',
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  badgeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 16,
    backgroundColor: 'rgba(150, 150, 150, 0.1)',
    marginBottom: 12,
  }
});
